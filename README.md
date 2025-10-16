# Added by Kevin Stallone:

## Next steps/TODO

1. Switched to gpt-image-1 and results are much improved. ~~Generate a better image for marketing. I believe the chain is generating a prompt that is too detailed and or literal. This is something I don't have a tremendous amount of experience with and need to investigate more. The prompt can be seen here:~~
> ~~"Design a visually appealing image that captures the user journey of purchasing a scooter from Target without using any words. The image should be highly engaging and suitable for sharing on social platforms. It should convey the user's actions of searching, scrolling, selecting, adding to cart, and dragging to checkout. Use creative elements and colors to represent the different steps of the journey. Keep the image under 1000 characters including whitespace to ensure optimal social media compatibility."~~ 
2. Expand the Pydantic model to include more of the fields and talk with other engineers to determine with fields are truly optional and which are required
3. Implement FastAPI endpoint(s) to allow the backend to process more than just one local flow.json. I imagine it being a put endpoint with some user selectable options (such as ignoring cache). It'd return the markdown report for any given flow.json
4. Implement a better caching system/database. Given the uniqueness of flow.jsons there could be multiple approaches. If we don't see a ton of variety, maybe use Postgres tables to store extracted info from the flow.jsons and generated AI summaries. If we anticipate a ton of variety, then probably a redis db with a ttl so if the same flow.json is uploaded within a specific time period we can serve the cached markdown file and image.
5. Dockerize the pipeline. Once FastAPI is implemented with a caching system we like, create a Dockerfile to create an image that we can deploy

## Project Structure

### Source Code Organization (`src/`)

The project is organized into modules for better maintainability:

```
src/
├── main.py                                    # Main entry point - runs complete analysis pipeline
└── arcade_flow_analyzer/
    ├── __init__.py                           # Package initialization and exports
    ├── models.py                             # Pydantic data models for flow validation
    ├── extractors/                           # Data extraction modules
    │   ├── __init__.py
    │   ├── extractor.py                      # Main flow data extraction logic
    │   └── basic_extractor.py                # Basic extraction used for testing
    ├── analysis/                             # Data processing & AI summarization
    │   ├── __init__.py
    │   ├── csv_preprocessor.py               # CSV preprocessing for AI analysis
    │   └── summarize.py                      # AI-powered summarization (chain & agentic)
    └── visualization/                        # Image generation
        ├── __init__.py
        └── image_gen.py                      # gpt-image-1 image generation
```

### Cache Structure (`cache/`)

The application uses caching to avoid redundant inference API calls to OpenAI:

```
cache/
├── actions.csv                               # Extracted user actions from flow.json
├── processed_actions.csv                     # Preprocessed CSV for AI analysis
├── ai-steps-chain.txt                        # AI-generated step-by-step user journey
├── ai-summary-chain.txt                      # AI-generated narrative summary
├── ai-summary-agentic.txt                    # Alternative agentic approach summary
└── image/                                    # Image generation cache
    ├── image-description.txt                 # AI-generated image prompt (unused)
    ├── image-url.txt                         # DALL-E generated image URL (unused)
    ├── generated-image.png                   # Downloaded image file (DALL-E Image; unused)
    └── marking-image.png                     # Downloaded image file (Igpt-image-1; used)
```

### Running the Pipeline

The complete analysis pipeline can be run with:

```bash
poetry run python3 src/main.py
```

This executes the following steps:
1. **Extract** actions from `flow.json` → save to `cache/actions.csv`
2. **Summarize** user journey using AI → generate steps and summary files
3. **Visualize** flow with Image API and gpt-image-1 → create marketing image
4. **Report** → combine all results into timestamped markdown file


# Arcade AI Interview Challenge

Welcome to the Arcade AI Interview Challenge! This project tests your ability to work with AI multimodal APIs, and be creative with your problem solving

## 🎯 Challenge Overview

You've been provided with a `flow.json` file that contains data from an Arcade flow recording. Your task is to build a script that analyzes this flow data and creates a comprehensive report.

## 📋 Requirements

Your application should accomplish the following:

1. **Identify User Interactions**: List out the actions the user did in a human readable format (i.e. "Clicked on checkout", "Search for X")
2. **Generate Human-Friendly Summary**: Create a clear, readable summary of what the user was trying to accomplish
3. **Create a Social Media Image**: Generate an creative image suitable for sharing on social platforms that represents the flow and would drive engagement

These items should be then displayed in a **markdown file** that can be committed in your project

## 🛠️ Technical Requirements

- **Language**: Any
- **AI Integration**: You will be provided an OpenAI API key, but feel free to use providers you have accounts with
- **Version Control**: Use GitHub/Bitbucket to track your work - we want to see your development process and commit history

## 🔒 Security Note

**IMPORTANT**: Never commit your API key to version control! Use environment variables or a `.env` file (and add it to `.gitignore`) to keep your API key secure.

## 📁 Project Structure

You'll be provided with:
- `flow.json` - The flow data to analyze
- OpenAI API key 


Your application should generate:
- A comprehensive markdown report
- A social media image file

## 🎨 Arcade Flow Reference

The flow data comes from this Arcade recording: https://app.arcade.software/share/2RnSqfsV4EsODmUiPKoW

You can view the original flow to understand what the user was doing, your solution should be general purpose enough to work for most Arcade flows.

## 💡 Hints

- The `flow.json` contains different types of steps (IMAGE, CHAPTER, VIDEO, etc.)
- Each step has metadata about what the user clicked and when
- Think about how to structure your analysis for maximum clarity
- The social media image should be professional and represent the flow's purpose
- Feel free to use different models types to both understand the flow and generate the image

## 💰 Cost Management

We do have API limits, and since you'll likely run this script multiple times during development and testing, we strongly recommend implementing caching for expensive API responses.

This will help you stay within API rate limits and keep costs manageable while iterating on your solution.


## Good luck! 
We're excited to see your creative approach to this challenge.
