help: # Lists commands
	@awk 'BEGIN { print "Available commands:"; } \
		 /^##/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 3); next; } \
		 /^[a-zA-Z0-9_-]+:/ { \
			 split($$0, parts, /:.*#/); \
			 cmd = parts[1]; \
			 sub(/^[ \t]+/, "", cmd); \
			 desc = substr($$0, index($$0, "#") + 1); \
			 if (desc != "") \
				 printf "\033[36m%-30s\033[0m %s\n", cmd, desc; \
		 }' $(MAKEFILE_LIST)

start-lama: # Starts the docker container which hosts lama
	docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama

pull-models: # Downloads and sets up llama3.2 and nomic-embed-text for usage
	docker exec -it ollama ollama pull llama3.2
	docker exec -it ollama ollama pull nomic-embed-text

install: # Installs Python Deps
	pip install -r requirements.txt

run: # Runs the program
	python main.py
