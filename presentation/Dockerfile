FROM node:18

# Set npm cache to reduce repeated downloads
RUN mkdir /npm_cache && npm config set cache /npm_cache

# Install marp-cli globally
RUN npm install -g @marp-team/marp-cli

WORKDIR /app

EXPOSE 5001
CMD ["marp", "-s", ".", "--port", "5001"]
