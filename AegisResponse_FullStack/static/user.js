const $=id=>document.getElementById(id),form=$("reportForm");
let selectedFile=null,cameraStream=null,previewUrl=null;

function setPhotoMessage(message){$("photoMsg").textContent=message}
function showPreview(file){
  if(previewUrl)URL.revokeObjectURL(previewUrl);
  previewUrl=URL.createObjectURL(file);
  $("preview").src=previewUrl;
  $("preview").hidden=false;
}
function stopCamera(){
  if(cameraStream){cameraStream.getTracks().forEach(track=>track.stop());cameraStream=null}
  $("cameraPreview").srcObject=null;
  $("cameraPreview").hidden=true;
  $("cameraStart").disabled=false;
  $("cameraCapture").disabled=true;
  $("cameraStop").disabled=true;
}
function acceptPhoto(file){
  if(!file)return;
  if(!["image/jpeg","image/png","image/webp"].includes(file.type)){
    setPhotoMessage("Choose a JPG, PNG or WEBP image.");return;
  }
  if(file.size>8*1024*1024){setPhotoMessage("Image must be 8 MB or smaller.");return}
  selectedFile=file;
  showPreview(file);
  setPhotoMessage("Photo ready. Select Analyse photo to fill the report suggestions.");
}
$("photo").addEventListener("change",()=>acceptPhoto($("photo").files[0]));
$("cameraStart").onclick=async()=>{
  if(!navigator.mediaDevices?.getUserMedia){
    setPhotoMessage("Camera access is unavailable. Use the photo upload option instead.");return;
  }
  try{
    cameraStream=await navigator.mediaDevices.getUserMedia({video:{facingMode:{ideal:"environment"}},audio:false});
    $("cameraPreview").srcObject=cameraStream;
    $("cameraPreview").hidden=false;
    $("cameraStart").disabled=true;
    $("cameraCapture").disabled=false;
    $("cameraStop").disabled=false;
    setPhotoMessage("Camera is ready. Capture the emergency scene.");
  }catch(err){
    setPhotoMessage(err.name==="NotAllowedError"?"Camera permission was denied. Allow camera access or upload a photo.":"Unable to open camera. Try uploading a photo instead.");
    stopCamera();
  }
};
$("cameraCapture").onclick=()=>{
  const video=$("cameraPreview");
  if(!cameraStream||!video.videoWidth){setPhotoMessage("Wait until the camera preview is ready.");return}
  const canvas=document.createElement("canvas");
  canvas.width=video.videoWidth;canvas.height=video.videoHeight;
  canvas.getContext("2d").drawImage(video,0,0,canvas.width,canvas.height);
  canvas.toBlob(blob=>{
    if(!blob){setPhotoMessage("Could not capture the image. Please try again.");return}
    acceptPhoto(new File([blob],"emergency-capture.jpg",{type:"image/jpeg"}));
    stopCamera();
    $("photo").value="";
    setPhotoMessage("Photo captured. Select Analyse photo to fill the report suggestions.");
  },"image/jpeg",0.88);
};
$("cameraStop").onclick=()=>{stopCamera();setPhotoMessage("Camera closed.")};
async function analyseSelectedPhoto(){
  if(!selectedFile){setPhotoMessage("Take a photo or choose an image first.");return}
  const fd=new FormData();fd.append("photo",selectedFile,"emergency-photo."+((selectedFile.type.split("/")[1]||"jpeg").replace("jpeg","jpg")));
  $("analyse").disabled=true;setPhotoMessage("Analysing photo…");
  try{
    const r=await fetch("/api/analyse-image",{method:"POST",body:fd});
    const d=await r.json();
    if(!r.ok)throw Error(d.error||"Photo analysis failed.");
    for(const k of ["title","description","category","severity"])if(d[k])form.elements[k].value=d[k];
    setPhotoMessage("Suggestions added to the form. Review and correct them before submitting.");
  }catch(e){setPhotoMessage(e.message)}
  finally{$("analyse").disabled=false}
}
$("analyse").onclick=analyseSelectedPhoto;
$("gps").onclick=()=>{
  if(!navigator.geolocation){alert("GPS is not supported.");return}
  navigator.geolocation.getCurrentPosition(p=>{
    $("lat").value=p.coords.latitude.toFixed(6);$("lon").value=p.coords.longitude.toFixed(6);
    $("location").value=$("location").value||"GPS location";
  },()=>alert("Location permission denied. Enter location manually."));
};
$("voice").onclick=()=>{
  const SR=window.SpeechRecognition||window.webkitSpeechRecognition;
  if(!SR){alert("Voice input is not supported in this browser.");return}
  const rec=new SR();rec.lang="en-IN";
  rec.onresult=e=>{form.elements.description.value=(form.elements.description.value+" "+e.results[0][0].transcript).trim()};
  rec.start();
};
form.onsubmit=async e=>{
  e.preventDefault();
  const d=Object.fromEntries(new FormData(form));
  for(const k of ["latitude","longitude"])d[k]=d[k]?Number(d[k]):null;
  d.people=Number(d.people||0);$("result").textContent="Submitting…";
  try{
    const r=await fetch("/api/incidents",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(d)});
    const j=await r.json();if(!r.ok)throw Error(j.error||"Submission failed");
    $("result").textContent=`Report received. Reference: ${j.item.id}. Priority score: ${j.item.priority_score}/99.`;
    form.reset();$("preview").hidden=true;selectedFile=null;stopCamera();
    if(previewUrl){URL.revokeObjectURL(previewUrl);previewUrl=null}
    setPhotoMessage("");
  }catch(err){$("result").textContent=err.message}
};
window.addEventListener("beforeunload",stopCamera);
