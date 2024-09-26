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

lama-start: # Starts the docker container which hosts lama
	docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama

run-lama32: # Downloads and sets up llama3.2 for usage
	docker exec -it ollama ollama run llama3.2

install: # Installs Python Deps
	pip install -r requirements.txt

run: # Runs the program
	python main.py
