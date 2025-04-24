#choose an official image
# FROM node:18-alpine AS base
FROM node:23-alpine AS base

#create a work directory
WORKDIR /app

#copy dependency based on the JS package manager used
COPY package.json yarn.lock* package-lock.json* pnpm-lock.yaml* ./

#install based on the projects package manager
RUN \
    if [ -f yarn.lock ]; then yarn --frozen-lockfile; \ 
    elif [ -f package-lock.json ]; then npm ci; \
    elif [ -f pnpm-lock.yaml ]; then corepack enable pnpm && pnpm i --frozen-lockfile; \
    else echo "No lock file found. Exiting..." && exit 1; \
    fi

#copy other application files to the working directory of the container
COPY . .

#create a build directory
RUN npm run build

#expose the application on port 3000
EXPOSE 3000

#run the application
CMD ["npm", "start"]