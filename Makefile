all: build
	docker run -e OPENAI_API_KEY --rm -p 5000:5000 -v ./data:/data haqs
build:
	docker build -t haqs . 