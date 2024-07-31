const button1 = document.getElementsByClassName('button')[0];
const button2 = document.getElementsByClassName('button')[1];
const button3 = document.getElementsByClassName('button')[2];
const button4 = document.getElementsByClassName('button')[3];

const buttondecode1 = document.getElementsByClassName('button-decode')[0];
const buttondecode2 = document.getElementsByClassName('button-decode')[1];
const buttondecode3 = document.getElementsByClassName('button-decode')[2];
const buttondecode4 = document.getElementsByClassName('button-decode')[3];

const img = document.querySelector('.image-hide');
img.style.display = 'none';

const audio = document.querySelector('.audio-hide');
audio.style.display = 'none';

const vid = document.querySelector('.video-hide');
vid.style.display = 'none';

const text = document.querySelector('.text-hide');
text.style.display = 'none';

const imgdecode = document.querySelector('.image-extract');
imgdecode.style.display = 'none';

const audiodecode = document.querySelector('.audio-extract');
audiodecode.style.display = 'none';



const textdecode = document.querySelector('.text-extract');
textdecode.style.display = 'none';

const div1 = document.getElementsByClassName('intro')[0];
const div2 = document.getElementsByClassName('encoding')[0];
const div3 = document.getElementsByClassName('decoding')[0];

button1.addEventListener('click',()=>{
    div1.style.display ='none';
    div2.style.display ='none';
    div3.style.display ='none';
    img.style.display = 'block';
})

button2.addEventListener('click',()=>{
    div1.style.display ='none';
    div2.style.display ='none';
    div3.style.display ='none';
    audio.style.display = 'block';
})

button3.addEventListener('click',()=>{
    div1.style.display ='none';
    div2.style.display ='none';
    div3.style.display ='none';
    vid.style.display = 'block';
})

button4.addEventListener('click',()=>{
    div1.style.display ='none';
    div2.style.display ='none';
    div3.style.display ='none';
    text.style.display = 'block';
})

buttondecode1.addEventListener('click',()=>{
    div1.style.display ='none';
    div2.style.display ='none';
    div3.style.display ='none';
    imgdecode.style.display = 'block';
})

buttondecode2.addEventListener('click',()=>{
    div1.style.display ='none';
    div2.style.display ='none';
    div3.style.display ='none';
    audiodecode.style.display = 'block';
})

buttondecode4.addEventListener('click',()=>{
    div1.style.display ='none';
    div2.style.display ='none';
    div3.style.display ='none';
    textdecode.style.display = 'block';
})

