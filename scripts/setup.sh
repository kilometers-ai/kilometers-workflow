#!/bin/bash
# Make this script executable: chmod +x scripts/setup.sh
# Setup script for kilometers-workflow

echo "🚀 Setting up kilometers-workflow development environment..."

# Check for required tools
check_command() {
    if ! command -v $1 &> /dev/null; then
        echo "❌ $1 is not installed. Please install it first."
        exit 1
    fi
}

echo "📋 Checking prerequisites..."
check_command python3
check_command docker
check_command docker-compose
check_command git

# Create Python virtual environment
echo "🐍 Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "🔐 Creating .env file..."
    cat > .env << EOL
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Database Configuration
DATABASE_URL=postgresql://postgres:password@localhost:5432/kilometers_workflow

# Redis Configuration
REDIS_URL=redis://localhost:6379

# Notification Services (optional)
TELEGRAM_BOT_TOKEN=
DISCORD_WEBHOOK_URL=

# Monitoring
PHOENIX_API_KEY=
AGENTOPS_API_KEY=

# Environment
ENVIRONMENT=development
LOG_LEVEL=INFO
EOL
    echo "⚠️  Please update .env with your actual API keys"
fi

# Initialize git hooks (optional)
echo "🔗 Setting up git hooks..."
cat > .git/hooks/pre-commit << 'EOL'
#!/bin/bash
# Run formatters and linters
source venv/bin/activate
black . --check
ruff .
EOL
chmod +x .git/hooks/pre-commit

# Create necessary directories
echo "📁 Creating additional directories..."
mkdir -p logs
mkdir -p data/artifacts
mkdir -p data/checkpoints

# Pull Docker images
echo "🐳 Pulling required Docker images..."
docker-compose pull

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Update .env with your API keys"
echo "2. Activate virtual environment: source venv/bin/activate"
echo "3. Start services: docker-compose up -d"
echo "4. Run the API: uvicorn services.api_gateway.main:app --reload"
echo ""
echo "📚 See docs/guides/getting-started.md for detailed instructions"
