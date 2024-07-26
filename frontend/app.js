const button1 = document.getElementsByClassName('button')[0];
const button2 = document.getElementsByClassName('button')[1];
const button3 = document.getElementsByClassName('button')[2];
const button4 = document.getElementsByClassName('button')[3];

const img = document.querySelector('.image-hide');
img.style.display = 'none';

const audio = document.querySelector('.audio-hide');
audio.style.display = 'none';

const vid = document.querySelector('.video-hide');
vid.style.display = 'none';

const text = document.querySelector('.text-hide');
text.style.display = 'none';

const div1 = document.getElementsByClassName('intro')[0];
const div2 = document.getElementsByClassName('encoding')[0];

button1.addEventListener('click',()=>{
    div1.style.display ='none';
    div2.style.display ='none';
    img.style.display = 'block';
})

button2.addEventListener('click',()=>{
    div1.style.display ='none';
    div2.style.display ='none';
    audio.style.display = 'block';
})

button3.addEventListener('click',()=>{
    div1.style.display ='none';
    div2.style.display ='none';
    vid.style.display = 'block';
})

button4.addEventListener('click',()=>{
    div1.style.display ='none';
    div2.style.display ='none';
    text.style.display = 'block';
})

const dropArea = document.getElementById("drop-area");
const inputFile = document.getElementById("input-file");
const imageView = document.getElementById("img-view");

inputFile.addEventListener("change" , uploadImage);

function uploadImage() {
    let imgLink = URL.createObjectURL(inputFile.files[0]);
    imageView.style.backgroundImage = `url('${imgLink}')`;
    imageView.textContent = "";
    imageView.style.border = 0;
}

dropArea.addEventListener("dragover",function(e){
    e.preventDefault();
});

dropArea.addEventListener("drop" , function(e){
    e.preventDefault();
    inputFile.files = e.dataTransfer.files;
});
