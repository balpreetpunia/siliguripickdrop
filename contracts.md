# Backend Implementation Contracts - Siliguri Pick Drop

## Overview
Implement backend API for booking management with MongoDB storage and Gmail email notifications.

## Environment Variables (.env)
```
GMAIL_USER=siliguripickdrop@gmail.com
GMAIL_APP_PASSWORD=tmdh agar khfi szqe
```

## MongoDB Schema
**Collection: bookings**
```python
{
    "_id": ObjectId,
    "booking_id": str,  # UUID
    "name": str,
    "phone": str,
    "email": str (optional),
    "service_type": str,
    "pickup_location": str,
    "drop_location": str,
    "date": str,
    "time": str,
    "notes": str,
    "status": str (default: "pending"),
    "created_at": datetime,
    "updated_at": datetime
}
```

## API Endpoints

### POST /api/bookings
**Request Body:**
```json
{
    "name": "string",
    "phone": "string",
    "email": "string",
    "service_type": "string",
    "pickup_location": "string",
    "drop_location": "string",
    "date": "string",
    "time": "string",
    "notes": "string"
}
```

**Response:**
```json
{
    "success": true,
    "message": "Booking request submitted successfully",
    "booking_id": "uuid"
}
```

### GET /api/bookings (optional - for admin)
Returns list of all bookings

## Email Notification
- Send to: siliguripickdrop@gmail.com
- Subject: "New Booking Request - Siliguri Pick Drop"
- Include: All booking details in formatted HTML

## Frontend Integration
- Remove mock.js usage
- Update BookingForm.jsx to call POST /api/bookings
- Use REACT_APP_BACKEND_URL from .env

## Implementation Files
1. /app/backend/.env - Add email credentials
2. /app/backend/server.py - Add booking routes and email logic
3. /app/frontend/src/components/BookingForm.jsx - Replace mock with API call
