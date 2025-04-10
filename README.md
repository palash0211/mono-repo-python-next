# Full-Stack Enterprise Monorepo

This is a monorepo containing a Next.js 15 frontend (SPA mode) with enterprise structure, FastAPI backend with enterprise structure, and Terraform infrastructure code for AWS deployment.

## Project Structure

```
📁 .
├── 📁 apps/
│   ├── 📁 backend/             # FastAPI backend
│   │   ├── 📁 app/             # Main application code
│   │   │   ├── 📁 api/         # API routes and endpoints
│   │   │   ├── 📁 core/        # Core functionality (config, security)
│   │   │   ├── 📁 db/          # Database setup and session management
│   │   │   ├── 📁 middleware/  # API middlewares
│   │   │   ├── 📁 models/      # SQLAlchemy models
│   │   │   ├── 📁 schemas/     # Pydantic schemas
│   │   │   ├── 📁 services/    # Business logic services
│   │   │   └── 📁 utils/       # Utility functions
│   │   ├── 📁 migrations/      # Alembic database migrations
│   │   ├── 📁 tests/           # Backend tests
│   │   ├── main.py             # Application entry point
│   │   └── requirements.txt    # Python dependencies
│   │
│   └── 📁 frontend/            # Next.js frontend
│       ├── 📁 app/             # Next.js app router
│       │   ├── 📁 (auth)/      # Authentication pages
│       │   ├── 📁 (protected)/ # Protected pages
│       │   ├── 📁 api/         # API route handlers
│       │   └── layout.tsx      # Root layout
│       ├── 📁 components/      # UI components
│       │   ├── 📁 ui/          # Shadcn UI components
│       │   └── 📁 shared/      # Shared components
│       ├── 📁 lib/             # Utility libraries
│       │   ├── 📁 redux/       # Redux store and slices
│       │   ├── 📁 hooks/       # Custom React hooks
│       │   └── 📁 utils/       # Utility functions
│       ├── 📁 public/          # Static assets
│       ├── 📁 styles/          # Global styles
│       └── 📁 types/           # TypeScript type definitions
│
├── 📁 infrastructure/          # Terraform IaC
│   ├── 📁 modules/             # Terraform modules
│   │   ├── 📁 backend/         # Backend infrastructure
│   │   ├── 📁 database/        # Database infrastructure
│   │   ├── 📁 frontend/        # Frontend infrastructure
│   │   └── 📁 vpc/             # Network infrastructure
│   ├── main.tf                 # Main Terraform configuration
│   ├── variables.tf            # Terraform variables
│   └── outputs.tf              # Terraform outputs
│
├── package.json                # Root package.json with dependencies
├── turbo.json                  # Turborepo configuration
└── README.md                   # Project documentation
```

## Features

- **Frontend**
  - Next.js 15 with App Router
  - Redux state management with Redux Toolkit
  - Form validation with Zod
  - UI components with shadcn/ui and Tailwind CSS
  - Authentication with JWT tokens
  - Protected routes with middleware

- **Backend**
  - FastAPI with enterprise architecture
  - SQLAlchemy ORM for database interaction
  - JWT authentication with OAuth2
  - Role-based access control
  - API documentation with Swagger UI
  - Service-based architecture

- **Infrastructure**
  - AWS cloud deployment
  - VPC with public and private subnets
  - RDS PostgreSQL database
  - ECS Fargate for backend
  - S3 and CloudFront for frontend
  - Security groups and IAM roles

## Getting Started

### Prerequisites

- Node.js 18+
- Python 3.10+
- AWS CLI configured
- Terraform 1.0+

### Development

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. Install dependencies:
   ```bash
   # Install root dependencies
   npm install

   # Install frontend dependencies
   cd apps/frontend
   npm install

   # Install backend dependencies
   cd ../backend
   pip install -r requirements.txt
   ```

3. Start development servers:
   ```bash
   # From root directory
   npm run dev
   ```

### Infrastructure Deployment

1. Initialize Terraform:
   ```bash
   cd infrastructure
   terraform init
   ```

2. Plan deployment:
   ```bash
   terraform plan -var="db_password=your-secure-password"
   ```

3. Apply deployment:
   ```bash
   terraform apply -var="db_password=your-secure-password"
   ```

## Testing

```bash
# Run frontend tests
cd apps/frontend
npm run test

# Run backend tests
cd ../backend
pytest
```

## Deployment

The application can be deployed using the Terraform scripts provided in the infrastructure directory.

## License

MIT