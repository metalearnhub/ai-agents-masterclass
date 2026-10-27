"""Add a post to the /blog list. Usage: python3 tools/blog_patch.py <ignored_get_page_file> <slug> "<H1>" "<blurb>"
Since Oct 27 2026 the list is a card list built from pages/blog/list.json by tools/blog_list.py; the get_page file is no longer needed (kept for compatibility).
Writes blog_patch.json -> patch_page(51cab93b-..., dry_run=false), then publish_page(custom_path blog)."""
import os,subprocess,sys
sys.exit(subprocess.call([sys.executable,os.path.join(os.path.dirname(os.path.abspath(__file__)),'blog_list.py')]+sys.argv[2:5]))
