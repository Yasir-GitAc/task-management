const messageModal = document.querySelector(".message-modal")
const messageModalCloseBtn = document.querySelector(".message-modal-close-btn")
console.log(messageModal)
console.log(messageModalCloseBtn)

if (messageModal){
  console.log('from if :',messageModal)
  messageModalCloseBtn.addEventListener('click', ()=>{
    console.log('clicked')
    messageModal.classList.add('message-modal-hide');
    console.log('message modal hidden')
  })
}
