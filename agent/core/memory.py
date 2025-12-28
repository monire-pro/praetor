import time
import json
import os
from datetime import datetime

class AgentMemory:
    def __init__(self):
        # 1. In-Memory List (This is what the React Frontend fetches)
        self.stream = []
        
        # 2. Local Backup File (Optional, keeps history if you restart server)
        self.file_path = "logs_history.json"
        
        # Load previous logs if they exist
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r") as f:
                    self.stream = json.load(f)
            except:
                self.stream = []

    def add_thought(self, tag: str, description: str):
        """
        Logs a specific step or thought from the agent.
        
        Args:
            tag (str): The category (e.g., "PLANNING", "SUCCESS", "ERROR", "COMMAND")
            description (str): The detailed text of what is happening.
        """
        
        entry = {
            "timestamp": time.time(), # Standard Unix timestamp
            "tag": tag.upper(),       # Ensure tags are uppercase for the frontend styling
            "description": description
        }

        # Add to the in-memory list
        self.stream.append(entry)

        # Optimization: Only keep the last 200 logs to prevent RAM bloat
        if len(self.stream) > 200:
            self.stream.pop(0)

        # Save to disk (for backup)
        self._save_to_disk()
        
        # Print to terminal so you can see it working in the background
        print(f"🧠 [{tag}] {description}")

    def _save_to_disk(self):
        """Helper to save logs to a local JSON file."""
        try:
            with open(self.file_path, "w") as f:
                json.dump(self.stream, f, indent=2)
        except Exception as e:
            print(f"⚠️ Memory Save Error: {e}")

    def get_recent_thoughts(self):
        """Returns the list of logs for the API."""
        # Return reversed copy if you want newest first, 
        # or standard list if Frontend handles sorting.
        return self.stream