#!/usr/bin/env python3
"""
Backend API Testing for Siliguri Pick Drop Booking System
Tests all backend endpoints and functionality
"""

import requests
import json
import time
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/app/frontend/.env')

# Get backend URL from frontend environment
BACKEND_URL = os.getenv('REACT_APP_BACKEND_URL', 'http://localhost:8001')
API_BASE = f"{BACKEND_URL}/api"

print(f"Testing backend at: {API_BASE}")

class BookingAPITester:
    def __init__(self):
        self.test_results = {
            'passed': 0,
            'failed': 0,
            'errors': []
        }
        
    def log_result(self, test_name, success, message=""):
        if success:
            self.test_results['passed'] += 1
            print(f"✅ {test_name}: PASSED {message}")
        else:
            self.test_results['failed'] += 1
            self.test_results['errors'].append(f"{test_name}: {message}")
            print(f"❌ {test_name}: FAILED - {message}")
    
    def test_health_check(self):
        """Test basic API connectivity"""
        try:
            response = requests.get(f"{API_BASE}/", timeout=10)
            if response.status_code == 200:
                self.log_result("Health Check", True, f"Status: {response.status_code}")
                return True
            else:
                self.log_result("Health Check", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_result("Health Check", False, f"Connection error: {str(e)}")
            return False
    
    def test_create_booking_valid(self):
        """Test POST /api/bookings with valid data"""
        booking_data = {
            "name": "Rajesh Kumar",
            "phone": "+91-9876543210",
            "email": "rajesh.kumar@email.com",
            "service_type": "airport-pickup",
            "pickup_location": "Siliguri City Center",
            "drop_location": "Bagdogra Airport (IXB)",
            "date": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
            "time": "10:30 AM",
            "notes": "Flight arrives at 11:00 AM, please be on time"
        }
        
        try:
            response = requests.post(
                f"{API_BASE}/bookings",
                json=booking_data,
                headers={"Content-Type": "application/json"},
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and data.get('booking_id'):
                    self.log_result("Create Booking (Valid Data)", True, 
                                  f"Booking ID: {data.get('booking_id')}, Email sent: {data.get('email_sent')}")
                    return data.get('booking_id')
                else:
                    self.log_result("Create Booking (Valid Data)", False, 
                                  f"Invalid response structure: {data}")
                    return None
            else:
                self.log_result("Create Booking (Valid Data)", False, 
                              f"Status: {response.status_code}, Response: {response.text}")
                return None
                
        except Exception as e:
            self.log_result("Create Booking (Valid Data)", False, f"Error: {str(e)}")
            return None
    
    def test_create_booking_minimal(self):
        """Test POST /api/bookings with minimal required fields"""
        booking_data = {
            "name": "Priya Sharma",
            "phone": "+91-8765432109",
            "service_type": "njp-drop",
            "pickup_location": "Siliguri Junction",
            "drop_location": "New Jalpaiguri Railway Station",
            "date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        }
        
        try:
            response = requests.post(
                f"{API_BASE}/bookings",
                json=booking_data,
                headers={"Content-Type": "application/json"},
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and data.get('booking_id'):
                    self.log_result("Create Booking (Minimal Data)", True, 
                                  f"Booking ID: {data.get('booking_id')}")
                    return data.get('booking_id')
                else:
                    self.log_result("Create Booking (Minimal Data)", False, 
                                  f"Invalid response: {data}")
                    return None
            else:
                self.log_result("Create Booking (Minimal Data)", False, 
                              f"Status: {response.status_code}, Response: {response.text}")
                return None
                
        except Exception as e:
            self.log_result("Create Booking (Minimal Data)", False, f"Error: {str(e)}")
            return None
    
    def test_create_booking_invalid(self):
        """Test POST /api/bookings with invalid/missing data"""
        
        # Test 1: Missing required fields
        invalid_data = {
            "name": "Test User"
            # Missing phone, service_type, pickup_location, drop_location, date
        }
        
        try:
            response = requests.post(
                f"{API_BASE}/bookings",
                json=invalid_data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code in [400, 422]:  # Expected validation error
                self.log_result("Create Booking (Missing Fields)", True, 
                              f"Correctly rejected with status: {response.status_code}")
            else:
                self.log_result("Create Booking (Missing Fields)", False, 
                              f"Should reject but got status: {response.status_code}")
                
        except Exception as e:
            self.log_result("Create Booking (Missing Fields)", False, f"Error: {str(e)}")
        
        # Test 2: Empty request body
        try:
            response = requests.post(
                f"{API_BASE}/bookings",
                json={},
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code in [400, 422]:
                self.log_result("Create Booking (Empty Body)", True, 
                              f"Correctly rejected with status: {response.status_code}")
            else:
                self.log_result("Create Booking (Empty Body)", False, 
                              f"Should reject but got status: {response.status_code}")
                
        except Exception as e:
            self.log_result("Create Booking (Empty Body)", False, f"Error: {str(e)}")
        
        # Test 3: Malformed JSON
        try:
            response = requests.post(
                f"{API_BASE}/bookings",
                data="invalid json",
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code in [400, 422]:
                self.log_result("Create Booking (Malformed JSON)", True, 
                              f"Correctly rejected with status: {response.status_code}")
            else:
                self.log_result("Create Booking (Malformed JSON)", False, 
                              f"Should reject but got status: {response.status_code}")
                
        except Exception as e:
            self.log_result("Create Booking (Malformed JSON)", False, f"Error: {str(e)}")
    
    def test_get_bookings(self):
        """Test GET /api/bookings endpoint"""
        try:
            response = requests.get(f"{API_BASE}/bookings", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and 'bookings' in data:
                    bookings = data.get('bookings', [])
                    self.log_result("Get Bookings", True, 
                                  f"Retrieved {len(bookings)} bookings")
                    
                    # Verify booking structure if bookings exist
                    if bookings:
                        booking = bookings[0]
                        required_fields = ['booking_id', 'name', 'phone', 'service_type', 
                                         'pickup_location', 'drop_location', 'date', 'status']
                        missing_fields = [field for field in required_fields if field not in booking]
                        
                        if not missing_fields:
                            self.log_result("Booking Data Structure", True, 
                                          "All required fields present")
                        else:
                            self.log_result("Booking Data Structure", False, 
                                          f"Missing fields: {missing_fields}")
                    
                    return True
                else:
                    self.log_result("Get Bookings", False, f"Invalid response structure: {data}")
                    return False
            else:
                self.log_result("Get Bookings", False, 
                              f"Status: {response.status_code}, Response: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Get Bookings", False, f"Error: {str(e)}")
            return False
    
    def test_email_functionality(self):
        """Test email notification by checking backend logs"""
        print("\n📧 Testing Email Functionality:")
        print("Creating a booking to trigger email notification...")
        
        # Create a booking that should trigger email
        booking_data = {
            "name": "Email Test User",
            "phone": "+91-9999888777",
            "email": "test@example.com",
            "service_type": "airport-drop",
            "pickup_location": "Siliguri Hotel",
            "drop_location": "Bagdogra Airport",
            "date": (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d"),
            "time": "2:00 PM",
            "notes": "Email functionality test"
        }
        
        try:
            response = requests.post(
                f"{API_BASE}/bookings",
                json=booking_data,
                headers={"Content-Type": "application/json"},
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                email_sent = data.get('email_sent', False)
                
                if email_sent:
                    self.log_result("Email Notification", True, 
                                  "Email sent successfully according to API response")
                else:
                    self.log_result("Email Notification", False, 
                                  "API indicates email was not sent")
                
                # Check backend logs for email confirmation
                print("Checking backend logs for email confirmation...")
                self.check_backend_logs()
                
            else:
                self.log_result("Email Notification", False, 
                              f"Booking creation failed: {response.status_code}")
                
        except Exception as e:
            self.log_result("Email Notification", False, f"Error: {str(e)}")
    
    def check_backend_logs(self):
        """Check backend supervisor logs for email confirmation"""
        try:
            import subprocess
            result = subprocess.run(
                ["tail", "-n", "50", "/var/log/supervisor/backend.out.log"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                log_content = result.stdout
                if "Email sent successfully" in log_content:
                    self.log_result("Email Log Verification", True, 
                                  "Found 'Email sent successfully' in backend logs")
                else:
                    print("📋 Recent backend logs:")
                    print(log_content[-500:])  # Show last 500 chars
                    self.log_result("Email Log Verification", False, 
                                  "No 'Email sent successfully' message found in logs")
            else:
                print("Could not read backend logs")
                
        except Exception as e:
            print(f"Error checking logs: {str(e)}")
    
    def run_all_tests(self):
        """Run all backend tests"""
        print("🚀 Starting Siliguri Pick Drop Backend API Tests")
        print("=" * 60)
        
        # Test 1: Health check
        if not self.test_health_check():
            print("❌ Backend is not accessible. Stopping tests.")
            return self.get_summary()
        
        print("\n📝 Testing Booking Creation...")
        
        # Test 2: Valid booking creation
        booking_id1 = self.test_create_booking_valid()
        
        # Test 3: Minimal data booking
        booking_id2 = self.test_create_booking_minimal()
        
        # Test 4: Invalid data handling
        self.test_create_booking_invalid()
        
        print("\n📋 Testing Booking Retrieval...")
        
        # Test 5: Get bookings
        self.test_get_bookings()
        
        print("\n📧 Testing Email Notifications...")
        
        # Test 6: Email functionality
        self.test_email_functionality()
        
        return self.get_summary()
    
    def get_summary(self):
        """Get test summary"""
        total_tests = self.test_results['passed'] + self.test_results['failed']
        
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {self.test_results['passed']}")
        print(f"❌ Failed: {self.test_results['failed']}")
        
        if self.test_results['errors']:
            print("\n🚨 FAILED TESTS:")
            for error in self.test_results['errors']:
                print(f"  • {error}")
        
        success_rate = (self.test_results['passed'] / total_tests * 100) if total_tests > 0 else 0
        print(f"\n📈 Success Rate: {success_rate:.1f}%")
        
        return {
            'total': total_tests,
            'passed': self.test_results['passed'],
            'failed': self.test_results['failed'],
            'errors': self.test_results['errors'],
            'success_rate': success_rate
        }

if __name__ == "__main__":
    tester = BookingAPITester()
    results = tester.run_all_tests()
    
    # Exit with error code if tests failed
    if results['failed'] > 0:
        exit(1)
    else:
        print("\n🎉 All tests passed!")
        exit(0)