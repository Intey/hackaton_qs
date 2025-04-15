FROM node:18

# Install marp-cli globally
RUN npm install -g @marp-team/marp-cli

WORKDIR /app

EXPOSE 5001
CMD ["marp", "-s", ".", "--port", "5001"]
