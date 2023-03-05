function show_form(){
    var board = document.getElementById('bill_board')
    var f = document.getElementById('form')
    if(board.style.display == "none"){
        f.style.display = "none"
        board.style.display = "block"
    }
    else{
        f.style.display = "flex"
        board.style.display = "none"
    }
}

function home(){
    window.location.reload()
}

// document.getElementById('bid_button').addEventListener('click' , show_form)