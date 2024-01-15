# Use an official Node runtime as a parent image
FROM node:21

# Set the working directory in the container
WORKDIR /frontend

ENV NODE_ENV=development

# Copy the current directory contents into the container at /frontend
COPY ./frontend ./

# Install any needed packages
RUN npm install

# Build
RUN npm run build

# Serve frontend
CMD ["npm", "run", "preview"]
