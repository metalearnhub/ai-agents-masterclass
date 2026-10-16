import sys,subprocess
sys.path.insert(0,'.')
import svgs
css=open('/home/claude/autopilot/tools/style.css').read()
html='<html><head><style>'+css+'</style></head><body style="width:640px;margin:0"><div class="dd-article">'+svgs.LEAK+svgs.FLOW+'</div></body></html>'
open('/tmp/claude-0/-home-claude/a0ddebc3-1c9f-5dc3-9d51-6b734607f315/scratchpad/figs.html','w').write(html)
