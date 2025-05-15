# Airport Reservation System (ARS)

A comprehensive Odoo module for managing airline reservations and flight operations. This module provides a complete solution for managing flight bookings, passenger information, aircraft details, and ticket generation with integrated invoicing capabilities.

## Features

- **Flight Management**
  - Schedule and track flights
  - Monitor flight status (draft, pending, departed, completed, cancelled)
  - Track actual departure and arrival times
  - Manage aircraft assignments
  - Real-time seat availability tracking

- **Booking System**
  - Create and manage flight reservations
  - Automated booking reference generation
  - Multi-passenger booking support
  - Integrated passenger management
  - Real-time seat availability checking

- **Ticket Management**
  - Automated ticket generation
  - Individual passenger ticket tracking
  - Integrated pricing system
  - Digital ticket management

- **Financial Integration**
  - Automated invoice generation
  - Integrated payment tracking
  - Financial reporting capabilities
  - Multiple currency support

- **Airport Operations**
  - Airport information management
  - Route management
  - Flight scheduling

## Technical Requirements

- Odoo 16.0 or later
- Python 3.8 or later
- Required Odoo modules:
  - base
  - mail
  - account
  - hr

## Installation

1. Clone the repository or download the module
2. Place the `ars` folder in your Odoo addons directory
3. Update the Odoo apps list
4. Install the module through the Odoo interface
   - Navigate to Apps
   - Search for "Airport Reservation System"
   - Click Install

## Module Structure

```
ars/
├── models/
│   ├── account_move.py
│   ├── ars_aircraft.py
│   ├── ars_airport.py
│   ├── ars_employee.py
│   ├── ars_flight.py
│   ├── ars_passenger.py
│   ├── ars_reservation.py
│   └── ars_ticket.py
├── security/
│   └── ir.model.access.csv
├── views/
│   ├── ars_aircraft_views.xml
│   ├── ars_flight_views.xml
│   ├── ars_menus.xml
│   ├── ars_passenger_views.xml
│   ├── ars_reservation_views.xml
│   └── ars_ticket_views.xml
├── wizards/
│   ├── ars_reservation_wizard.py
│   └── ars_reservation_wizard.xml
└── __manifest__.py
```

## Usage

1. **Flight Creation**
   - Create and schedule new flights
   - Assign aircraft
   - Set departure and arrival airports
   - Define seat capacity and pricing

2. **Booking Process**
   - Create new bookings for single or multiple passengers
   - Select flights and verify seat availability
   - Input passenger information
   - Generate tickets automatically

3. **Ticket Management**
   - View and manage ticket details
   - Track ticket status
   - Generate invoices
   - Process payments

4. **Reporting**
   - Access flight schedules
   - View booking statistics
   - Track revenue and occupancy rates
   - Monitor flight status

## Dependencies

- base: Base Odoo functionalities
- mail: Communication and notification features
- account: Invoicing and payment management
- hr: Employee management integration

## Version

Current version: 0.1

## Author

KenjxJJ

## Support

For support and bug reports, please create an issue in the repository or contact the module author.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This module is released under the [LGPL-3](https://www.gnu.org/licenses/lgpl-3.0.en.html) license.
