# Chess

A turn-based chess game with full move validation, castling, and pawn promotion — built using Python and Pygame. The game features intuitive piece selection, legal move highlighting, and a modular structure for future multiplayer or AI integration.

![Chess Screenshot](assets/images/screenshot.png) <!-- Replace with actual path to your screenshot -->

---

## 🧠 Tech Stack

- **Language:** Python 3.10+
- **Library:** [Pygame](https://www.pygame.org/)
- **Architecture:** Modular object-oriented structure (scenes, board, rules, UI)

---

## 🚀 Features

- Standard 8x8 chess board with all legal pieces  
- Legal move highlighting (blue tiles)  
- Castling (king and rook)  
- Pawn promotion to queen  
- Clean GUI using Pygame  
- Game result detection (checkmate, stalemate in progress)  
- Modular design for easy expansion

---

## 📦 Installation & Running

```bash
# Clone the repository
git clone https://github.com/ALyS123/Chess.git
cd Chess

# Optional: Create a virtual environment
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows

# Install dependencies
pip install pygame

# Run the game
python main.py
```

---

## 🎮 Gameplay Controls

- **Select a piece**: Click on a piece to highlight its valid moves  
- **Move a piece**: Click on a highlighted square  
- **Exit the game**: Press `Esc` or close the window  

---

## 📁 Repository Structure

```text
Chess/
├── assets/           # Piece images and sounds
├── board/            # Board setup, movement logic, rule engine
├── core/             # Input and scene handling
├── pieces/           # Piece initialization and movement
├── scenes/           # Menu and in-game scenes
├── settings.py       # Game configuration (window, colors, etc.)
├── main.py           # Entry point
```

---

## 🛠 Future Improvements

- Implement AI opponent (Minimax or Monte Carlo Tree Search)  
- Add en passant and draw condition detection  
- Create a main menu and in-game pause/restart options  
- Add move history, timers, and score tracking  
- Online multiplayer using sockets or REST API  

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
