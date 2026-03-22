# Soulmate AI Chat App

## Overview

This project is an AI-powered chat application where users create a personalized “soulmate” (male or female) with selected attributes such as name, traits, and religion. The backend generates a realistic AI image of the soulmate and maintains a continuous conversation using an LLM. The system can also generate new images (poses) of the same character during the chat to enhance engagement.

---

## Tech Stack

* **Frontend:** Vue 3 (Composition API)
* **Backend:** FastAPI
* **AI Models:** Gemini (text + image generation)
* **Storage:** Local static image storage

---

## Project Structure

### Backend (`/backend/app`)

#### `main.py`

Initializes the FastAPI app, registers routes, enables CORS, and mounts the `/images` static directory.

#### `api/chat.py`

Handles chat logic:

* Receives user messages
* Manages session state
* Triggers AI replies
* Sends images/offers at specific message intervals

#### `api/upload.py`

Handles user image uploads (used for couple image generation).

---

### Services (`/services`)

#### `gemini_service.py`

Handles text generation:

* Builds personality prompt
* Sends messages to Gemini
* Returns short, flirty responses

#### `wife_generator.py` (now Soulmate Generator)

Core AI logic:

* Generates soulmate profile (name, traits, religion)
* Generates base AI image
* Generates new poses from the same base image
* Saves images locally and returns URLs

#### `session_manager.py`

Tracks:

* Session IDs
* Message counts
* Flags (image sent, offer sent, etc.)

#### `image_service.py`

Generates combined images (user + soulmate), used for couple-style outputs.

---

### Frontend (`/frontend/src`)

#### `App.vue`

Main controller:

* Displays selector first
* Passes selected data to chat
* Switches between setup and chat views

#### `components/SoulmateSelector.vue`

User setup screen:

* Fetches available options from backend
* Lets user choose name, traits, religion
* Emits selected data to parent

#### `components/Chat.vue`

Chat interface:

* Sends messages to backend
* Displays AI responses
* Renders images and offers
* Maintains session state

---

## Flow

1. User selects soulmate attributes
2. Backend generates soulmate + base image
3. Chat starts with AI personality
4. System sends:

   * Text replies (LLM)
   * Images (generated from base)
   * Offers (based on message count)
5. Session persists behavior and progression

---

## Notes

* Images are stored locally in `/app/static/images`
* Gemini API is used for both text and image generation
* Rate limits may apply depending on API plan

---

## Future Improvements

* Database integration (users, sessions, images)
* Better UI/UX (mobile-first, animations)
* Payment/monetization flow
* Image caching and CDN support
