const loading = document.querySelector('#loading')
const app = document.querySelector('#app')
const theme_switch = document.querySelector('#theme-switch')
const htmTag = document.querySelector('html')
const moon = document.querySelector('.moon')
const sun = document.querySelector('.sun')
const menu = document.querySelector('#menu')
const section_two = document.querySelector('.section-two')


menu.addEventListener('click', ()=>{
    section_two.classList.toggle('section-two-hov')
})



window.addEventListener('DOMContentLoaded', ()=>{
    loading.classList.add('display-none');
    app.classList.remove('display-none');
})

const savedTheme  = localStorage.getItem('theme')
if (savedTheme){
    htmTag.setAttribute('dark-mode', savedTheme );
};

theme_switch.addEventListener('click', ()=>{
    const currentTheme = htmTag.getAttribute('dark-mode');
    const nextTheme = currentTheme === 'dark' ? 'light' : 'dark'
    htmTag.setAttribute('dark-mode', nextTheme);
    localStorage.setItem('theme', nextTheme);
    
})

