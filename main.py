import os
import sys

import uvicorn

sys.path.insert(1, os.path.join(sys.path[0], "src"))


if __name__ == "__main__":
    uvicorn.run("app:create_app", factory=True, reload=True)
