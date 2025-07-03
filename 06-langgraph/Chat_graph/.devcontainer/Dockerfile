# FROM mcr.microsoft.com/devcontainers/python:3.12

# ENV PYTHONUNBUFFERED=1

# RUN sudo apt-get update && \
#     sudo apt-get install -y curl

# RUN pip install --upgrade pip

# # Install Poetry
# RUN curl -sSL https://install.python-poetry.org | python3 -

# # Add Poetry to PATH

# ENV PATH=/root/.local/bin:$PATH

# ✅ Base Image: Official Microsoft Dev Container Python 3.12
FROM mcr.microsoft.com/devcontainers/python:3.12

# ✅ Make Python output unbuffered (for logs)
ENV PYTHONUNBUFFERED=1

# ✅ Install curl and other common tools
RUN sudo apt-get update && \
    sudo apt-get install -y curl git

# ✅ Upgrade pip
RUN pip install --upgrade pip

# ✅ Install Poetry (Optional - if you're using pyproject.toml)
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# ✅ Install core GenAI-related Python packages
RUN pip install \
    langchain \
    openai \
    pymongo \
    qdrant-client \
    redis \
    tiktoken

# ✅ Set default working directory inside container
WORKDIR /workspaces
