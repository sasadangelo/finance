# ETF Manager - Flask Application

Flask web application for managing an ETF portfolio with complete CRUD functionality.

## Project Structure

```
finance/
├── app.py                      # Main Flask application
├── database.py                 # SQLAlchemy database configuration
├── models/                     # Database models (DAO)
│   ├── __init__.py
│   └── etf.py                 # ETF model
├── services/                   # Business logic layer
│   ├── __init__.py
│   └── etf_service.py         # ETF management services
├── controllers/                # Controllers for routes
│   ├── __init__.py
│   └── etf_controller.py      # ETF controller
├── routes/                     # Route definitions
│   └── etf_routes.py          # ETF routes
├── templates/                  # HTML templates
│   ├── base.html              # Base template
│   └── etf/
│       ├── index.html         # ETF list
│       ├── create.html        # Create ETF form
│       ├── edit.html          # Edit ETF form
│       └── show.html          # ETF details
└── static/                     # Static files (CSS, JS)
    ├── css/
    └── js/
```

## Architecture

The application follows the **MVC (Model-View-Controller)** pattern with a service layer:

1. **Models** (`models/`): Define data structure and interact with the database
2. **Services** (`services/`): Contain business logic and CRUD operations
3. **Controllers** (`controllers/`): Handle HTTP requests and coordinate models and views
4. **Routes** (`routes/`): Define application endpoints
5. **Templates** (`templates/`): HTML views with Jinja2

## CRUD Functionality

### List ETFs
- **URL**: `/` or `/etfs`
- **Method**: GET
- **Description**: Display all ETFs in the database

### Create ETF
- **URL**: `/etfs/create`
- **Method**: GET
- **Description**: Show form to create a new ETF

### Store ETF
- **URL**: `/etfs/store`
- **Method**: POST
- **Description**: Save a new ETF to the database

### Show ETF
- **URL**: `/etfs/<ticker>`
- **Method**: GET
- **Description**: Display details of a specific ETF

### Edit ETF
- **URL**: `/etfs/<ticker>/edit`
- **Method**: GET
- **Description**: Show form to edit an ETF

### Update ETF
- **URL**: `/etfs/<ticker>/update`
- **Method**: POST
- **Description**: Update an existing ETF

### Delete ETF
- **URL**: `/etfs/<ticker>/delete`
- **Method**: POST
- **Description**: Delete an ETF from the database

## Getting Started

### Prerequisites
- Python 3.12+
- UV package manager

### Installation
```bash
# Install dependencies
uv sync
```

### Running the Application
```bash
# Start the Flask application
uv run python app.py
```

The application will be available at: http://127.0.0.1:5001

### Alternative: Using Flask CLI
```bash
# Alternative using Flask CLI
uv run flask run --port 5001
```

## ETF Data Model

```python
class Etf:
    ticker: str              # ETF ticker (primary key)
    name: str               # ETF name
    isin: str               # ISIN code
    launchDate: str         # Launch date
    capital: float          # Capital in millions
    replication: str        # Replication type
    volatility: float       # Volatility percentage
    currency: str           # Currency
    dividend: str           # Dividend type (Distribution/Accumulation)
    dividendFrequency: int  # Dividend frequency (1=Annual, 2=Semi-annual, 4=Quarterly, 12=Monthly)
    yeld: float            # Yield percentage
```

## Technologies Used

- **Flask**: Python web framework
- **SQLAlchemy**: ORM for database
- **SQLite**: Database
- **Bootstrap 5**: CSS framework
- **Font Awesome**: Icons
- **Jinja2**: Template engine

## Development Notes

- Port 5000 might be occupied by AirPlay Receiver on macOS, so the app uses port 5001
- SQLite database is located at `database/etfs.db`
- Flash messages are used for user feedback
- All forms include client-side and server-side validation

## Future Enhancements

- [ ] User authentication
- [ ] REST API for external integration
- [ ] Export data to CSV/Excel
- [ ] Charts and statistics
- [ ] Integration with automatic quote download
- [ ] Dashboard with portfolio metrics