// Mock data for frontend-only testing

export const mockBookingSubmit = async (bookingData) => {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 800));
  
  // Store in localStorage for demo
  const bookings = JSON.parse(localStorage.getItem('bookings') || '[]');
  const newBooking = {
    ...bookingData,
    id: Date.now().toString(),
    submittedAt: new Date().toISOString(),
    status: 'pending'
  };
  bookings.push(newBooking);
  localStorage.setItem('bookings', JSON.stringify(bookings));
  
  return { success: true, booking: newBooking };
};

export const serviceData = {
  airportServices: [
    {
      route: 'Airport (Bagdogra/IXB) ↔ Siliguri (within 15km)',
      price: '₹600',
      details: 'One-way trip'
    },
    {
      route: 'Airport (Bagdogra/IXB) ↔ Siliguri (within 20km)',
      price: '₹700',
      details: 'One-way trip'
    }
  ],
  railwayServices: [
    {
      route: 'NJP Station ↔ Siliguri City',
      price: '₹500',
      details: 'One-way trip'
    },
    {
      route: 'NJP Station ↔ Up to 5km outside Siliguri',
      price: '₹600',
      details: 'One-way trip'
    }
  ],
  vehicle: {
    model: '2018 Maruti Suzuki Brezza',
    color: 'White',
    features: ['Air Conditioned', 'Comfortable Seating', 'Clean & Well Maintained', 'Experienced Driver']
  },
  contact: {
    phone: '9002336919',
    email: 'siliguripickdrop@gmail.com'
  }
};