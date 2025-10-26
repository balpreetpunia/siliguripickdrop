import React, { useState } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Textarea } from './ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { toast } from 'sonner';
import { mockBookingSubmit } from '../mock';
import { Calendar, MapPin, Phone, Mail, Clock } from 'lucide-react';

const BookingForm = () => {
  const [formData, setFormData] = useState({
    name: '',
    phone: '',
    email: '',
    serviceType: '',
    pickupLocation: '',
    dropLocation: '',
    date: '',
    time: '',
    notes: ''
  });
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSelectChange = (value) => {
    setFormData(prev => ({ ...prev, serviceType: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.name || !formData.phone || !formData.serviceType || !formData.date) {
      toast.error('Please fill in all required fields');
      return;
    }

    setIsSubmitting(true);
    try {
      const result = await mockBookingSubmit(formData);
      if (result.success) {
        toast.success('Booking request submitted! We will call you back soon.');
        // Reset form
        setFormData({
          name: '',
          phone: '',
          email: '',
          serviceType: '',
          pickupLocation: '',
          dropLocation: '',
          date: '',
          time: '',
          notes: ''
        });
      }
    } catch (error) {
      toast.error('Failed to submit booking. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Card className="w-full max-w-2xl mx-auto shadow-xl border-2 border-yellow-100">
      <CardHeader className="bg-gradient-to-r from-yellow-50 to-amber-50">
        <CardTitle className="text-3xl font-bold text-gray-900">Request a Booking</CardTitle>
        <CardDescription className="text-lg text-gray-700">
          Fill in the details and we'll call you back to confirm your trip
        </CardDescription>
      </CardHeader>
      <CardContent className="pt-6">
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-2">
              <Label htmlFor="name" className="text-base font-semibold text-gray-700">
                Full Name <span className="text-red-500">*</span>
              </Label>
              <Input
                id="name"
                name="name"
                value={formData.name}
                onChange={handleInputChange}
                placeholder="Enter your name"
                className="h-12 border-gray-300"
                required
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="phone" className="text-base font-semibold text-gray-700">
                Phone Number <span className="text-red-500">*</span>
              </Label>
              <div className="relative">
                <Phone className="absolute left-3 top-3.5 h-5 w-5 text-gray-400" />
                <Input
                  id="phone"
                  name="phone"
                  type="tel"
                  value={formData.phone}
                  onChange={handleInputChange}
                  placeholder="9002336919"
                  className="h-12 pl-10 border-gray-300"
                  required
                />
              </div>
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="email" className="text-base font-semibold text-gray-700">
              Email Address (Optional)
            </Label>
            <div className="relative">
              <Mail className="absolute left-3 top-3.5 h-5 w-5 text-gray-400" />
              <Input
                id="email"
                name="email"
                type="email"
                value={formData.email}
                onChange={handleInputChange}
                placeholder="your@email.com"
                className="h-12 pl-10 border-gray-300"
              />
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="serviceType" className="text-base font-semibold text-gray-700">
              Service Type <span className="text-red-500">*</span>
            </Label>
            <Select onValueChange={handleSelectChange} value={formData.serviceType}>
              <SelectTrigger className="h-12 border-gray-300">
                <SelectValue placeholder="Select service type" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="airport-pickup">Airport Pickup (Bagdogra/IXB)</SelectItem>
                <SelectItem value="airport-drop">Airport Drop (Bagdogra/IXB)</SelectItem>
                <SelectItem value="njp-pickup">NJP Station Pickup</SelectItem>
                <SelectItem value="njp-drop">NJP Station Drop</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-2">
              <Label htmlFor="pickupLocation" className="text-base font-semibold text-gray-700">
                <MapPin className="inline h-4 w-4 mr-1" />
                Pickup Location
              </Label>
              <Input
                id="pickupLocation"
                name="pickupLocation"
                value={formData.pickupLocation}
                onChange={handleInputChange}
                placeholder="e.g., Siliguri, Sukna, Salbari"
                className="h-12 border-gray-300"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="dropLocation" className="text-base font-semibold text-gray-700">
                <MapPin className="inline h-4 w-4 mr-1" />
                Drop Location
              </Label>
              <Input
                id="dropLocation"
                name="dropLocation"
                value={formData.dropLocation}
                onChange={handleInputChange}
                placeholder="e.g., Bagdogra Airport, NJP"
                className="h-12 border-gray-300"
              />
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-2">
              <Label htmlFor="date" className="text-base font-semibold text-gray-700">
                <Calendar className="inline h-4 w-4 mr-1" />
                Travel Date <span className="text-red-500">*</span>
              </Label>
              <Input
                id="date"
                name="date"
                type="date"
                value={formData.date}
                onChange={handleInputChange}
                className="h-12 border-gray-300"
                required
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="time" className="text-base font-semibold text-gray-700">
                <Clock className="inline h-4 w-4 mr-1" />
                Preferred Time
              </Label>
              <Input
                id="time"
                name="time"
                type="time"
                value={formData.time}
                onChange={handleInputChange}
                className="h-12 border-gray-300"
              />
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="notes" className="text-base font-semibold text-gray-700">
              Additional Notes
            </Label>
            <Textarea
              id="notes"
              name="notes"
              value={formData.notes}
              onChange={handleInputChange}
              placeholder="Any special requirements or instructions..."
              className="min-h-24 border-gray-300"
            />
          </div>

          <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 rounded">
            <p className="text-sm text-gray-700">
              <strong>Payment:</strong> Payment to be made via UPI or cash before the trip starts.
            </p>
          </div>

          <Button 
            type="submit" 
            disabled={isSubmitting}
            className="w-full h-14 text-lg font-bold bg-yellow-500 hover:bg-yellow-600 text-gray-900 shadow-lg transition-all duration-300 hover:scale-105"
          >
            {isSubmitting ? 'Submitting...' : 'Submit Booking Request'}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
};

export default BookingForm;