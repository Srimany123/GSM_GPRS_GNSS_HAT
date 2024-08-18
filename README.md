# GSM_GPRS_GNSS_HAT</br>

<p>
  this repository is use for the hat which supports gnss, gprs, gsm module. this repo mainly focus on gsm for now. my carrier is T-mobile.</br></br>
AT&T: wap.cingular</br>
T-Mobile: internet</br>
Verizon: vzwinternet</br>
MINT Mobile: wholesale</br>
<div>
  install nessary libraries first and update few permissions.</div></br>
  <pre>sudo bash start.sh</pre>
  before sending message or calling, we should check the what band the serial communication is going on.</br></br>
  <pre>./band_check.sh</pre>
  this will help us to identify which band the communication is going on.</br></br>
</div>
<div>
  the band i have used for communication is 115200, if you have different band, just type the below command to switch it back to 115200 through this command.</br></br>
  <pre>./switch_band.sh</pre>
</div>
<div>
  now that everything as set we can start using the message and phone options</br></br>
  start by using the phone.py, this is a simple mimic of phone, like sending message, calling a number like that.</br></br>
  <pre>python3 read_and_reply.py</pre>
  just play with the options you will completly figure it out.
</div>
</p>
