function sendMail(){
    let parms = {
        name : document.getElementById("name").value,
        email : document.getElementById("email").value,
        phone : document.getElementById("phone").value,
        interests : document.getElementById("interests").value,
        price : document.getElementById("price").value,
        cartlist: getCartList()
    }
    emailjs.send("service_3dghn9p","template_l3t414k",parms)
}

function getCartList() {
    const cart = JSON.parse(localStorage.getItem('cardCart')) || [];
    if (cart.length === 0) {
        return "No cards added to interested cart.";  // If there are no cards in the cart
    }
    
    // Format the cart list as a string
    return cart.map(card => `${card.first_name} ${card.last_name}`).join(', ');
}
