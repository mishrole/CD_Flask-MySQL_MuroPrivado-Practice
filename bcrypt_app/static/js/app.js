const radios = document.querySelectorAll('.radio-gender');
const otherInput = document.querySelector('#other');
const birthday = document.querySelector('#birthday');

radios.forEach((radio) => {
    radio.addEventListener('click', (e) => {
        if (e.target.value === 'Self describe') {
            otherInput.classList.remove('d-none');
            otherInput.focus();
        } else {
            otherInput.classList.add('d-none');
        }
    });
});

(function() {
    const today = new Date().toISOString().split('T')[0];
    birthday.setAttribute('max', today);
})();