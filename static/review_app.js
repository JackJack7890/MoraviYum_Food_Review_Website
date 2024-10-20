var dropdown_button1 = document.getElementById("activateDropdown1")
var dropdown_button2 = document.getElementById("activateDropdown2")

var dropdown1 = document.getElementById("dropdown1")
var dropdown2 = document.getElementById("dropdown2")

dropdown_button1.addEventListener('mouseover', () => {
    console.log('hovered')
    const dropdown = document.getElementById('dropdown1');
    dropdown.style.display = 'block';
})

dropdown_button1.addEventListener('mouseleave', () => {
    console.log('left hover');
    const dropdown = document.getElementById('dropdown1');
    dropdown.style.display = 'none';
});

dropdown_button2.addEventListener('mouseover', () =>{
    console.log('clicked2')
    const dropdown = document.getElementById('dropdown2');
    dropdown.style.display = 'block';
})

dropdown_button2.addEventListener('mouseleave', () => {
    console.log('left hover2');
    const dropdown = document.getElementById('dropdown2');
    dropdown.style.display = 'none';
})

dropdown1.addEventListener('mouseover', () => {
    console.log('hovered')
    const dropdown = document.getElementById('dropdown1');
    dropdown.style.display = 'block';
})

dropdown1.addEventListener('mouseleave', () => {
    console.log('left hover');
    const dropdown = document.getElementById('dropdown1');
    dropdown.style.display = 'none';
})

dropdown2.addEventListener('mouseover', () => {
    console.log('hovered')
    const dropdown = document.getElementById('dropdown2');
    dropdown.style.display = 'block';
})

dropdown2.addEventListener('mouseleave', () => {
    console.log('left hover');
    const dropdown = document.getElementById('dropdown2');
    dropdown.style.display = 'none';
})




