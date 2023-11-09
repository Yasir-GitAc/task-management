console.log('sanity check from task-handler')

document.addEventListener("DOMContentLoaded", function (){
  const ongoingTaskDiv = document.querySelector('#ongoingTask');
  if (ongoingTaskDiv) {
    ongoingTaskDiv.click();
  }
})

function getTaskModal(task) {
  console.log('Opening modal for task:', task);
  const taskModal = document.querySelector('.task-modal')
  const taskModalNavbar = taskModal.querySelector('.task-modal-navbar')
  const taskModalTitle = taskModalNavbar.querySelector('.task-modal-title')
  const taskModalCloseBtn = taskModalNavbar.querySelector('.task-modal-navbar-close-button')
  const taskModalMainSection = taskModal.querySelector('.task-modal-main-section')
  const taskDrescriptionText = taskModalMainSection.querySelector('.task-drescription-text')
  const taskPriorityText = taskModalMainSection.querySelector('.priority_text')
  const taskChecklistText = taskModalMainSection.querySelector('.checklist_text')
  const taskModalMainSidebar = taskModal.querySelector('.task-modal-main-sidebar')
  const companyLink = taskModalMainSidebar.querySelector('.company-anchor')
  const companyLogo = taskModalMainSidebar.querySelector('.company_logo')
  const companyName = taskModalMainSidebar.querySelector('.company-name')
  const statusText = taskModalMainSidebar.querySelector('.status-text')
  const finishingExpected = taskModalMainSidebar.querySelector('.finishing-expected')
  const dateCreated = taskModalMainSidebar.querySelector('.date-created')
  const finishingDate = taskModalMainSidebar.querySelector('.finishing-date')
  const taskAssigneeDiv = taskModalMainSidebar.querySelector('.task-modal-task-assignee-div')
  const taskEditBtn = taskModalMainSidebar.querySelector('.task-edit-button')

  const task_url = `http://127.0.0.1:8000/task/get-task-info-for-task-modal/${task.task_id}/`;

  fetch(task_url).then(response =>{
    return response.json()
  })
  .then(data =>{
    const task_info = data.data[0]
    console.log('task_info',task_info)
    taskModalNavbar.classList.remove('ongoing-task', 'finished-task', 'unstarted-task');
    taskModalNavbar.classList.add(`${task_info.status.toLowerCase()}-task`);

    taskModalTitle.textContent = task_info.title

    taskModalCloseBtn.classList.remove('ongoing-task-for-button', 'finished-task-for-button', 'unstarted-task-for-button')
    taskModalCloseBtn.classList.add(`${task_info.status.toLowerCase()}-task-for-button`);

    taskDrescriptionText.textContent = '';
    taskDrescriptionText.textContent = task_info.drescription

    taskPriorityText.textContent = '';
    taskPriorityText.textContent = task_info.priority

    taskChecklistText.textContent = '';
    taskChecklistText.textContent = task_info.checklist

    companyLink.href = `http://127.0.0.1:8000/company/company-profile/${task_info.company_id}/`;
    companyLogo.src = task_info.company_logo_url
    companyName.textContent = task_info.company;

    statusText.textContent = task_info.status;
    finishingExpected.textContent = task_info.finishing_expected;
    dateCreated.textContent = task_info.date_created;
    if(task_info.finishing_date){
      finishingDate.textContent = task_info.finishing_date[0]
    } else if (task_info.finishing_date===null){
      finishingDate.textContent = task_info.status
    }



    taskAssigneeDiv.innerHTML = '';
    taskAssigneeDiv.innerHTML = `<p class="assignee-div-title">Assignee :</p>`;

    const assignee_list = task_info.assignees

    assignee_list.forEach(assignee => {
      const assigneeAnchor = document.createElement('a');
      assigneeAnchor.href = `http://127.0.0.1:8000/account/user-profile/${assignee.assignee_id}`;

      const assigneeImage = document.createElement('img');
      assigneeImage.src = assignee.assignee_img_url;
      assigneeImage.classList.add('company_logo')
      assigneeImage.alt = 'profile_picture';

      const assigneeName = document.createElement('p');
      assigneeName.textContent = assignee.assignee_name;

      assigneeAnchor.appendChild(assigneeImage);
      assigneeAnchor.appendChild(assigneeName);

      taskAssigneeDiv.appendChild(assigneeAnchor);

    });

  })
  .catch(error => console.log(error))


  taskEditBtn.href = `http://127.0.0.1:8000/task/edit-task/${task.task_id}`;

  taskModal.classList.remove('hide-task-modal')

  taskModalCloseBtn.addEventListener('click', ()=>{
    taskModal.classList.add('hide-task-modal')
  })

}


function getTaskBasedOnStatus(status){
  console.log('button clicked')
  console.log('status', status)

  const tablebody = document.querySelector('.insert-data')
  tablebody.innerHTML = '';

  const url = `http://127.0.0.1:8000/task/get-task-info-based-on-status/${status}/`;

  fetch(url).then(response =>{
    return response.json()
  })
  .then(data =>{
    const task_list = data.data
    console.log('task_list',task_list)
    task_list.forEach(task => {
      const row = document.createElement("tr");

      const finishingExpected = document.createElement("td");
      finishingExpected.textContent = task.finishing_expected;
      row.appendChild(finishingExpected);

      const taskTitle = document.createElement("td");
      const title_link = document.createElement("a");
      title_link.textContent = task.title;
      taskTitle.appendChild(title_link)
      taskTitle.onclick = function() {
        getTaskModal(task);
      };
      row.appendChild(taskTitle);

      const priority = document.createElement("td");
      priority.textContent = task.priority;
      row.appendChild(priority);

      const company = document.createElement("td");
      const link = document.createElement("a");
      link.href = `/company/company-profile/${task.company_id}/`;
      link.textContent = task.company;
      company.appendChild(link);
      row.appendChild(company);


      tablebody.appendChild(row);
    });
  }).catch(error => console.log(error))

  const taskDiv = document.querySelector(`#${status}Task`);
  if (taskDiv) {taskDiv.classList.toggle('task-filter-div-active')};

  const allTaskDivs = document.querySelectorAll('.task-filter-div');
    allTaskDivs.forEach((div) => {
      if (div !== taskDiv) {
        div.classList.remove('task-filter-div-active');
      }
    });

}

//almost same as getTaskModal but slightly modified in term of style, and takes task id as only
// parameter, send from django templating language. whereas getTaskModal take task a jsonresponse as parameter.
// modal navbar color funtionality removed due to some inconsistency.


function getTaskModalById(task_id) {
  console.log('Opening modal for task:', task_id);
  const taskModal = document.querySelector('.task-modal')
  const taskModalNavbar = taskModal.querySelector('.task-modal-navbar')
  const taskModalTitle = taskModalNavbar.querySelector('.task-modal-title')
  const taskModalCloseBtn = taskModalNavbar.querySelector('.task-modal-navbar-close-button')
  const taskModalMainSection = taskModal.querySelector('.task-modal-main-section')
  const taskDrescriptionText = taskModalMainSection.querySelector('.task-drescription-text')
  const taskPriorityText = taskModalMainSection.querySelector('.priority_text')
  const taskChecklistText = taskModalMainSection.querySelector('.checklist_text')
  const taskModalMainSidebar = taskModal.querySelector('.task-modal-main-sidebar')
  const companyLink = taskModalMainSidebar.querySelector('.company-anchor')
  const companyLogo = taskModalMainSidebar.querySelector('.company_logo')
  const companyName = taskModalMainSidebar.querySelector('.company-name')
  const statusText = taskModalMainSidebar.querySelector('.status-text')
  const finishingExpected = taskModalMainSidebar.querySelector('.finishing-expected')
  const dateCreated = taskModalMainSidebar.querySelector('.date-created')
  const finishingDate = taskModalMainSidebar.querySelector('.finishing-date')
  const taskAssigneeDiv = taskModalMainSidebar.querySelector('.task-modal-task-assignee-div')
  const taskEditBtn = taskModalMainSidebar.querySelector('.task-edit-button')
  const taskDeleteBtn = taskModalMainSidebar.querySelector('.task-delete-button')

  const task_url = `http://127.0.0.1:8000/task/get-task-info-for-task-modal/${task_id}/`;

  fetch(task_url).then(response =>{
    return response.json()
  })
  .then(data =>{
    const task_info = data.data[0]
    console.log('task_info',task_info)

    taskModalTitle.textContent = task_info.title

    taskDrescriptionText.textContent = '';
    taskDrescriptionText.textContent = task_info.drescription

    taskPriorityText.textContent = '';
    taskPriorityText.textContent = task_info.priority

    taskChecklistText.textContent = '';
    taskChecklistText.textContent = task_info.checklist

    companyLink.href = `http://127.0.0.1:8000/company/company-profile/${task_info.company_id}/`;
    companyLogo.src = task_info.company_logo_url
    companyName.textContent = task_info.company;

    statusText.textContent = task_info.status;
    finishingExpected.textContent = task_info.finishing_expected;
    dateCreated.textContent = task_info.date_created;
    if(task_info.finishing_date){
      finishingDate.textContent = task_info.finishing_date[0]
    } else if (task_info.finishing_date===null){
      finishingDate.textContent = task_info.status
    }



    taskAssigneeDiv.innerHTML = '';
    taskAssigneeDiv.innerHTML = `<p class="assignee-div-title">Assignee :</p>`;

    const assignee_list = task_info.assignees

    assignee_list.forEach(assignee => {
      const assigneeAnchor = document.createElement('a');
      assigneeAnchor.href = `http://127.0.0.1:8000/account/user-profile/${assignee.assignee_id}`;

      const assigneeImage = document.createElement('img');
      assigneeImage.src = assignee.assignee_img_url;
      assigneeImage.classList.add('company_logo')
      assigneeImage.alt = 'profile_picture';

      const assigneeName = document.createElement('p');
      assigneeName.textContent = assignee.assignee_name;

      assigneeAnchor.appendChild(assigneeImage);
      assigneeAnchor.appendChild(assigneeName);

      taskAssigneeDiv.appendChild(assigneeAnchor);

    });

  })
  .catch(error => console.log(error))


  taskEditBtn.href = `http://127.0.0.1:8000/task/edit-task/${task_id}`;
  if(taskDeleteBtn){
    taskDeleteBtn.href = `http://127.0.0.1:8000/task/delete-task/${task_id}`;

  }

  taskModal.classList.remove('hide-task-modal')

  taskModalCloseBtn.addEventListener('click', ()=>{
    taskModal.classList.add('hide-task-modal')
  })

}
