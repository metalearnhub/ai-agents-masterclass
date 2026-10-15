def fig(id_,vb_h,title,desc,body,cap):
    return f'''<figure class="dd-fig">
<svg viewBox="0 0 640 {vb_h}" role="img" aria-labelledby="{id_}t {id_}d" xmlns="http://www.w3.org/2000/svg">
<title id="{id_}t">{title}</title>
<desc id="{id_}d">{desc}</desc>
<defs><marker id="{id_}a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#5b6470"/></marker></defs>
<rect x="0" y="0" width="640" height="{vb_h}" rx="14" fill="#f6f8fa"/>
{body}
</svg>
<figcaption><b>Figure N.</b> {cap}</figcaption>
</figure>'''
# JOURNEY: 5 stages, leak labels below
st=[('Inquiry','DM, call, form'),('Booking','date and time'),('Reminder','confirm or move'),('Visit','treatment'),('Review','and rebook')]
leaks=['Slow reply','Slow booking','No-show','','No review ask']
b=['<text x="24" y="34" class="svg-k">WHERE A CLINIC LOSES PATIENTS</text>']
w=104;g=18;x0=24
for i,(t,s) in enumerate(st):
    x=x0+i*(w+g)
    b.append(f'<rect x="{x}" y="58" width="{w}" height="62" rx="10" fill="{"#007a66" if i in (0,4) else "#e8f4f1"}" stroke="#007a66"/>')
    cls,cls2=('svg-w','svg-ws') if i in (0,4) else ('svg-t','svg-s')
    b.append(f'<text x="{x+w/2}" y="85" text-anchor="middle" class="{cls}">{t}</text><text x="{x+w/2}" y="104" text-anchor="middle" class="{cls2}">{s}</text>')
    if i<4: b.append(f'<path d="M{x+w+2} 89 L{x+w+g-2} 89" stroke="#5b6470" stroke-width="1.6" marker-end="url(#fj1a)"/>')
    if leaks[i]:
        b.append(f'<path d="M{x+w/2} 122 L{x+w/2} 150" stroke="#c2410c" stroke-width="1.6" stroke-dasharray="4 3" marker-end="url(#fj1a)"/>')
        b.append(f'<rect x="{x+4}" y="156" width="{w-8}" height="30" rx="8" fill="#fff4ec" stroke="#c2410c"/><text x="{x+w/2}" y="176" text-anchor="middle" class="svg-o">{leaks[i]}</text>')
b.append('<text x="24" y="216" class="svg-s">Automation fixes the four leaks. Staff keep the treatment advice and the visit.</text>')
JOURNEY=fig('fj1',236,'Where a clinic loses patients','Five stages from inquiry to booking, reminder, visit and review. Patients leak out at four points: slow replies to inquiries, slow back-and-forth while booking, no-shows after booking, and no review request after the visit.','\n'.join(b),'Four leaks between the first message and the next booking. Each one has an automation fix.')
# NOSHOW chart
def bar(y,label,val,color,txtcls='svg-w'):
    L=int(val/100*420)
    return f'<text x="24" y="{y+20}" class="svg-s">{label}</text><rect x="190" y="{y}" width="{L}" height="30" rx="6" fill="{color}"/><text x="{190+L-8}" y="{y+20}" text-anchor="end" class="{txtcls}">{val}%</text>'
b=['<text x="24" y="34" class="svg-k">BMJ OPEN META-ANALYSIS, 2016 (21 STUDIES)</text>',
   '<text x="24" y="64" class="svg-t">Attended the appointment</text>',
   bar(76,'Reminder sent',67,'#007a66'),bar(114,'No reminder',54,'#5b9e90'),
   '<text x="24" y="182" class="svg-t">Missed the appointment (no-show)</text>',
   bar(194,'Reminder sent',15,'#007a66'),bar(232,'No reminder',21,'#c2410c'),
   '<text x="24" y="292" class="svg-s">Source: BMJ Open 2016;6:e012116. Electronic notifications (text, voice, email).</text>']
NOSHOW=fig('fn1',312,'Reminders and attendance','Bar chart from a 2016 BMJ Open meta-analysis of 21 studies. Attendance was 67 percent with digital reminders versus 54 percent without. No-shows were 15 percent with reminders versus 21 percent without.','\n'.join(b),'Patients who got a digital reminder were about 25% less likely to miss their appointment.')
# REMIND timeline
pts=[(70,'Booked','Instant confirmation'),(220,'48 hours before','Confirm, move or cancel'),(390,'24 hours before','Prep instructions'),(550,'2 hours before','Address and parking')]
b=['<text x="24" y="34" class="svg-k">A SIMPLE REMINDER SCHEDULE</text>','<path d="M40 90 L612 90" stroke="#5b6470" stroke-width="1.6" marker-end="url(#fr1a)"/>']
for x,t,s in pts:
    b.append(f'<circle cx="{x}" cy="90" r="9" fill="#007a66"/><text x="{x}" y="66" text-anchor="middle" class="svg-t">{t}</text><text x="{x}" y="120" text-anchor="middle" class="svg-s">{s}</text>')
b.append('<rect x="160" y="140" width="320" height="34" rx="8" fill="#fff4ec" stroke="#c2410c"/><text x="320" y="162" text-anchor="middle" class="svg-o">No reply to the 48-hour message? Staff call.</text>')
REMIND=fig('fr1',196,'A simple reminder schedule','Timeline: instant confirmation when booked, a confirm-or-move message 48 hours before, prep instructions 24 hours before, address and parking 2 hours before. If the patient does not reply to the 48-hour message, staff call.','\n'.join(b),'Every reminder gives the patient an easy way to confirm or reschedule. A freed slot can be offered to the waitlist.')
