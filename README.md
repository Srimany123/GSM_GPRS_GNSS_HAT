# GSM_GPRS_GNSS_HAT</br>
<h3>GSM module</h3>
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
  <pre>python3 phone.py</pre>
  just play with the options you will completly figure it out.</br>
</div>
<div>
  now for advanced option, to store the messages and also store your replies for future use. like a smart phone does. bit confusing first. </br></br>
  <pre>python3 read_and_reply.py</pre>
  you might face and error, the location to store the messages does not exist also not enough permissions to make the file. in this case you have to manually create the file and give permission and also change the name of your desire file in the code.</br>
</div>
</p>
