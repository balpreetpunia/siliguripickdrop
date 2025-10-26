import React from 'react';
import { Phone, Mail, Car, MapPin, ArrowRight, CheckCircle, Navigation } from 'lucide-react';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import BookingForm from '../components/BookingForm';
import { serviceData } from '../mock';

const Home = () => {
  const scrollToBooking = () => {
    document.getElementById('booking-section').scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <div className="min-h-screen bg-white">
      {/* Header */}
      <header className="bg-gray-900 text-white sticky top-0 z-50 shadow-lg">
        <div className="container mx-auto px-4 py-4">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <div className="flex items-center gap-3">
              <Car className="h-8 w-8 text-yellow-400" />
              <h1 className="text-2xl md:text-3xl font-bold text-yellow-400">Siliguri Pick Drop</h1>
            </div>
            <div className="flex flex-col md:flex-row items-center gap-4 md:gap-6">
              <a href="tel:9002336919" className="flex items-center gap-2 hover:text-yellow-400 transition-colors">
                <Phone className="h-5 w-5" />
                <span className="font-semibold">9002336919</span>
              </a>
              <a href="mailto:siliguripickdrop@gmail.com" className="flex items-center gap-2 hover:text-yellow-400 transition-colors">
                <Mail className="h-5 w-5" />
                <span className="font-semibold">siliguripickdrop@gmail.com</span>
              </a>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative bg-gradient-to-br from-gray-50 via-yellow-50 to-amber-50 py-20 md:py-32">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center">
            <h2 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6 leading-tight">
              Reliable Airport & Railway Station
              <span className="text-yellow-600"> Transport Service</span>
            </h2>
            <p className="text-xl md:text-2xl text-gray-700 mb-8 leading-relaxed">
              Safe, comfortable, and affordable pick-up and drop services in <strong>Siliguri</strong>, <strong>Bagdogra (IXB)</strong>, and <strong>NJP Railway Station</strong>
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
              <Button 
                onClick={scrollToBooking}
                className="h-14 px-8 text-lg font-bold bg-yellow-500 hover:bg-yellow-600 text-gray-900 shadow-xl transition-all duration-300 hover:scale-105"
              >
                Book Your Ride <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
              <a href="https://wa.me/919002336919" target="_blank" rel="noopener noreferrer">
                <Button 
                  variant="outline"
                  className="h-14 px-8 text-lg font-bold border-2 border-yellow-500 text-gray-900 hover:bg-yellow-50 transition-all duration-300"
                >
                  WhatsApp Us
                </Button>
              </a>
            </div>
          </div>
        </div>
        <div className="absolute bottom-0 left-0 right-0 h-16 bg-gradient-to-t from-white to-transparent"></div>
      </section>

      {/* Services & Pricing Section */}
      <section className="py-16 md:py-24 bg-white">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h3 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">Our Services & Pricing</h3>
            <p className="text-lg text-gray-600">Transparent pricing, no hidden charges. One-way trips only.</p>
          </div>

          <div className="grid md:grid-cols-2 gap-8 max-w-5xl mx-auto">
            {/* Airport Services */}
            <Card className="shadow-xl border-2 border-yellow-100 hover:shadow-2xl transition-all duration-300">
              <CardHeader className="bg-gradient-to-r from-yellow-50 to-amber-50">
                <CardTitle className="text-2xl font-bold text-gray-900 flex items-center gap-2">
                  <Navigation className="h-6 w-6 text-yellow-600" />
                  Airport Services (Bagdogra/IXB)
                </CardTitle>
              </CardHeader>
              <CardContent className="pt-6">
                <div className="space-y-4">
                  {serviceData.airportServices.map((service, index) => (
                    <div key={index} className="p-4 bg-gray-50 rounded-lg border border-gray-200">
                      <div className="flex justify-between items-start mb-2">
                        <p className="font-semibold text-gray-900 flex-1">{service.route}</p>
                        <span className="text-2xl font-bold text-yellow-600 ml-4">{service.price}</span>
                      </div>
                      <p className="text-sm text-gray-600">{service.details}</p>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Railway Station Services */}
            <Card className="shadow-xl border-2 border-yellow-100 hover:shadow-2xl transition-all duration-300">
              <CardHeader className="bg-gradient-to-r from-yellow-50 to-amber-50">
                <CardTitle className="text-2xl font-bold text-gray-900 flex items-center gap-2">
                  <MapPin className="h-6 w-6 text-yellow-600" />
                  NJP Railway Station Services
                </CardTitle>
              </CardHeader>
              <CardContent className="pt-6">
                <div className="space-y-4">
                  {serviceData.railwayServices.map((service, index) => (
                    <div key={index} className="p-4 bg-gray-50 rounded-lg border border-gray-200">
                      <div className="flex justify-between items-start mb-2">
                        <p className="font-semibold text-gray-900 flex-1">{service.route}</p>
                        <span className="text-2xl font-bold text-yellow-600 ml-4">{service.price}</span>
                      </div>
                      <p className="text-sm text-gray-600">{service.details}</p>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>

          <div className="mt-8 text-center">
            <p className="text-sm text-gray-600 max-w-3xl mx-auto">
              Serving <strong>Siliguri, Sukna, Salbari</strong> and surrounding areas. Coverage includes all locations within the specified distance ranges.
            </p>
          </div>
        </div>
      </section>

      {/* Vehicle Section */}
      <section className="py-16 md:py-24 bg-gradient-to-br from-gray-50 to-yellow-50">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto">
            <div className="text-center mb-12">
              <h3 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">Our Vehicle</h3>
              <p className="text-lg text-gray-600">Travel in comfort and style</p>
            </div>

            <Card className="shadow-2xl border-2 border-yellow-200">
              <CardContent className="p-8">
                <div className="grid md:grid-cols-2 gap-8 items-center">
                  <div className="bg-gray-200 h-64 rounded-lg flex items-center justify-center">
                    <div className="text-center text-gray-500">
                      <Car className="h-24 w-24 mx-auto mb-4 text-gray-400" />
                      <p className="text-sm">2018 White Maruti Suzuki Brezza</p>
                      <p className="text-xs mt-2">(Actual vehicle photo placeholder)</p>
                    </div>
                  </div>
                  <div>
                    <h4 className="text-2xl font-bold text-gray-900 mb-4">{serviceData.vehicle.model}</h4>
                    <p className="text-lg text-gray-700 mb-6">Color: <span className="font-semibold">{serviceData.vehicle.color}</span></p>
                    <div className="space-y-3">
                      {serviceData.vehicle.features.map((feature, index) => (
                        <div key={index} className="flex items-center gap-3">
                          <CheckCircle className="h-5 w-5 text-yellow-600 flex-shrink-0" />
                          <span className="text-gray-700 font-medium">{feature}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Booking Section */}
      <section id="booking-section" className="py-16 md:py-24 bg-white">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h3 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">Book Your Ride</h3>
            <p className="text-lg text-gray-600">We'll call you back to confirm your booking</p>
          </div>
          <BookingForm />
        </div>
      </section>

      {/* Contact Section */}
      <section className="py-16 bg-gradient-to-r from-gray-900 to-gray-800 text-white">
        <div className="container mx-auto px-4 text-center">
          <h3 className="text-3xl font-bold mb-6">Need Immediate Assistance?</h3>
          <p className="text-xl mb-8">Call us or send a WhatsApp message</p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <a href="tel:9002336919">
              <Button className="h-14 px-8 text-lg font-bold bg-yellow-500 hover:bg-yellow-600 text-gray-900 transition-all duration-300">
                <Phone className="mr-2 h-5 w-5" />
                Call Now: 9002336919
              </Button>
            </a>
            <a href="https://wa.me/919002336919" target="_blank" rel="noopener noreferrer">
              <Button className="h-14 px-8 text-lg font-bold bg-green-600 hover:bg-green-700 text-white transition-all duration-300">
                WhatsApp Us
              </Button>
            </a>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-8 border-t border-gray-800">
        <div className="container mx-auto px-4">
          <div className="text-center">
            <div className="flex items-center justify-center gap-2 mb-4">
              <Car className="h-6 w-6 text-yellow-400" />
              <p className="text-xl font-bold text-yellow-400">Siliguri Pick Drop</p>
            </div>
            <p className="text-gray-400 mb-4">
              Reliable transport service for Bagdogra Airport (IXB), NJP Railway Station, and Siliguri region
            </p>
            <div className="flex flex-col sm:flex-row justify-center items-center gap-4 mb-4">
              <a href="tel:9002336919" className="flex items-center gap-2 hover:text-yellow-400 transition-colors">
                <Phone className="h-4 w-4" />
                9002336919
              </a>
              <span className="hidden sm:inline text-gray-600">|</span>
              <a href="mailto:siliguripickdrop@gmail.com" className="flex items-center gap-2 hover:text-yellow-400 transition-colors">
                <Mail className="h-4 w-4" />
                siliguripickdrop@gmail.com
              </a>
            </div>
            <p className="text-sm text-gray-500">
              © {new Date().getFullYear()} Siliguri Pick Drop. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Home;