from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
import uuid
from datetime import datetime, timezone
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# Define Models
class StatusCheck(BaseModel):
    model_config = ConfigDict(extra="ignore")  # Ignore MongoDB's _id field
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class StatusCheckCreate(BaseModel):
    client_name: str

# Booking Models
class BookingCreate(BaseModel):
    name: str
    phone: str
    email: Optional[str] = None
    service_type: str
    pickup_location: str
    drop_location: str
    date: str
    time: Optional[str] = None
    notes: Optional[str] = None

class Booking(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    booking_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    phone: str
    email: Optional[str] = None
    service_type: str
    pickup_location: str
    drop_location: str
    date: str
    time: Optional[str] = None
    notes: Optional[str] = None
    status: str = "pending"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# Email sending function
async def send_booking_email(booking: Booking):
    try:
        gmail_user = os.environ.get('GMAIL_USER')
        gmail_password = os.environ.get('GMAIL_APP_PASSWORD')
        
        if not gmail_user or not gmail_password:
            logger.error("Gmail credentials not found in environment variables")
            return False
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f'New Booking Request - Siliguri Pick Drop'
        msg['From'] = gmail_user
        msg['To'] = gmail_user
        
        # Service type mapping
        service_mapping = {
            'airport-pickup': 'Airport Pickup (Bagdogra/IXB)',
            'airport-drop': 'Airport Drop (Bagdogra/IXB)',
            'njp-pickup': 'NJP Station Pickup',
            'njp-drop': 'NJP Station Drop'
        }
        
        service_display = service_mapping.get(booking.service_type, booking.service_type)
        
        # Create HTML content
        html = f"""
        <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background-color: #FFD700; color: #000; padding: 20px; text-align: center; }}
                    .content {{ background-color: #f9f9f9; padding: 20px; border: 1px solid #ddd; }}
                    .field {{ margin-bottom: 15px; }}
                    .label {{ font-weight: bold; color: #555; }}
                    .value {{ color: #000; }}
                    .footer {{ text-align: center; padding: 15px; color: #777; font-size: 12px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h2>🚗 New Booking Request</h2>
                    </div>
                    <div class="content">
                        <div class="field">
                            <span class="label">Booking ID:</span>
                            <span class="value">{booking.booking_id}</span>
                        </div>
                        <div class="field">
                            <span class="label">Customer Name:</span>
                            <span class="value">{booking.name}</span>
                        </div>
                        <div class="field">
                            <span class="label">Phone Number:</span>
                            <span class="value">{booking.phone}</span>
                        </div>
                        {f'<div class="field"><span class="label">Email:</span><span class="value">{booking.email}</span></div>' if booking.email else ''}
                        <div class="field">
                            <span class="label">Service Type:</span>
                            <span class="value">{service_display}</span>
                        </div>
                        <div class="field">
                            <span class="label">Pickup Location:</span>
                            <span class="value">{booking.pickup_location}</span>
                        </div>
                        <div class="field">
                            <span class="label">Drop Location:</span>
                            <span class="value">{booking.drop_location}</span>
                        </div>
                        <div class="field">
                            <span class="label">Travel Date:</span>
                            <span class="value">{booking.date}</span>
                        </div>
                        {f'<div class="field"><span class="label">Preferred Time:</span><span class="value">{booking.time}</span></div>' if booking.time else ''}
                        {f'<div class="field"><span class="label">Additional Notes:</span><span class="value">{booking.notes}</span></div>' if booking.notes else ''}
                        <div class="field">
                            <span class="label">Submitted At:</span>
                            <span class="value">{booking.created_at.strftime('%d %B %Y, %I:%M %p')}</span>
                        </div>
                    </div>
                    <div class="footer">
                        <p>Siliguri Pick Drop - Reliable Transport Service</p>
                        <p>Please contact the customer to confirm the booking</p>
                    </div>
                </div>
            </body>
        </html>
        """
        
        # Attach HTML content
        msg.attach(MIMEText(html, 'html'))
        
        # Send email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(gmail_user, gmail_password)
            server.send_message(msg)
        
        logger.info(f"Email sent successfully for booking {booking.booking_id}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        return False

# Add your routes to the router instead of directly to app
@api_router.get("/")
async def root():
    return {"message": "Hello World"}

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.model_dump()
    status_obj = StatusCheck(**status_dict)
    
    # Convert to dict and serialize datetime to ISO string for MongoDB
    doc = status_obj.model_dump()
    doc['timestamp'] = doc['timestamp'].isoformat()
    
    _ = await db.status_checks.insert_one(doc)
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    # Exclude MongoDB's _id field from the query results
    status_checks = await db.status_checks.find({}, {"_id": 0}).to_list(1000)
    
    # Convert ISO string timestamps back to datetime objects
    for check in status_checks:
        if isinstance(check['timestamp'], str):
            check['timestamp'] = datetime.fromisoformat(check['timestamp'])
    
    return status_checks

# Booking Routes
@api_router.post("/bookings")
async def create_booking(booking_data: BookingCreate):
    try:
        # Create booking object
        booking = Booking(**booking_data.model_dump())
        
        # Convert to dict and serialize datetime to ISO string for MongoDB
        doc = booking.model_dump()
        doc['created_at'] = doc['created_at'].isoformat()
        doc['updated_at'] = doc['updated_at'].isoformat()
        
        # Insert into database
        result = await db.bookings.insert_one(doc)
        
        if result.inserted_id:
            logger.info(f"Booking created: {booking.booking_id}")
            
            # Send email notification (don't fail if email fails)
            email_sent = await send_booking_email(booking)
            
            return {
                "success": True,
                "message": "Booking request submitted successfully! We will call you back soon.",
                "booking_id": booking.booking_id,
                "email_sent": email_sent
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to create booking")
            
    except Exception as e:
        logger.error(f"Error creating booking: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/bookings")
async def get_bookings():
    try:
        bookings = await db.bookings.find({}, {"_id": 0}).to_list(1000)
        
        # Convert ISO string timestamps back to datetime objects
        for booking in bookings:
            if isinstance(booking.get('created_at'), str):
                booking['created_at'] = datetime.fromisoformat(booking['created_at'])
            if isinstance(booking.get('updated_at'), str):
                booking['updated_at'] = datetime.fromisoformat(booking['updated_at'])
        
        return {"success": True, "bookings": bookings}
        
    except Exception as e:
        logger.error(f"Error fetching bookings: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()