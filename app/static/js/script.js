const today = new Date();
let code = 0;
let search_id = 0;
let exp_data = '';


function checkAuthorization() {
    fetch('/api/protected/', {
        method: 'GET',
        credentials: 'include'  // Отправляем куки с запросом
    })
    .then(response =>   {
        if (response.status === 403) {
            let a = window.location
            if(a.pathname != "/") {}
            else{
                window.location.href = "auth/login/";  // Перенаправляем на логин
            }
        } else {
            // Пользователь авторизован, продолжаем работу
        return response.json();
        }
    })
    .then(data => {
        if (data) {
            console.log(data);
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
    })
}

checkAuthorization()

// Создание даты для поля "end_time", вычитая один день
const endDate = new Date(today);
endDate.setDate(endDate.getDate() - 1);

// Создание даты для поля "start_time" (первый день текущего месяца)
const startDate = new Date(today.getFullYear(), today.getMonth(), 1);

// Форматирование даты в строку формата 'YYYY-MM-DD'
function formatDate(date) {
    let day = date.getDate();
    let month = date.getMonth() + 1; // Месяцы начинаются с 0
    const year = date.getFullYear();

    if (day < 10) day = '0' + day;
    if (month < 10) month = '0' + month;

    return `${year}-${month}-${day}`;
}

// Установка значений в поля ввода
if(window.location.pathname == "/") {
    document.getElementById('end_time').value = formatDate(endDate);
    document.getElementById('start_time').value = formatDate(startDate);
}




function logout() {
    window.location.replace('/auth/logout/');
}

let search_input = document.getElementById('search-input')
if(search_input){

    document.getElementById('search-input').addEventListener('input', function() {
        const query = this.value; // Получаем значение из поля ввода
        const resultsContainer = document.getElementById('search-results');

        if (query.length > 0) { 
            fetch(`/api/life_search/?employee_icontains=${query}`, {
                credentials: 'include'
            })
            .then(response => {
                if (response.status === 403) {
                    alert("Срок сессии истёк")
                    logout(); // Вызов функции logout при статусе 403
                    throw new Error('Unauthorized'); // Останавливаем дальнейшую обработку
                }
                return response.json();
            })
            .then(data => {
                resultsContainer.innerHTML = ''; // Очищаем предыдущие результаты

                data.data.forEach(item => {
                    const div = document.createElement('div');
                    div.classList.add('search-result');
                    const span = document.createElement('span');
                    if (parseInt(item.emp_code) < 10) {
                        span.textContent = `${item.emp_code}    ${item.first_name}`;
                    } else if (parseInt(item.emp_code) < 100) {
                        span.textContent = `${item.emp_code} ${item.first_name}`;
                    }
                    div.appendChild(span);
                    div.addEventListener('click', function() {
                        document.getElementById('search-input').value = item.first_name; // Заполняем поле ввода выбранным значением
                        search_id = item.id;
                        resultsContainer.innerHTML = ''; // Очищаем результаты после выбора
                    });
                    resultsContainer.appendChild(div);
                });
            })
            .catch(error => {
                console.error('Ошибка:', error);
            });
        } else {
            resultsContainer.innerHTML = ''; 
            search_id = 0;
        }
    });
}

function empReport(start_time, end_time) {
    const params = {};

    const startDate = new Date(start_time);
    const endDate = new Date(end_time);
    const now = new Date();

    // Проверка и установка end_time
    if (endDate > now) {
        params["end_time"] = now.toISOString().split('T')[0];
    } else {
        params["end_time"] = end_time;
    }

    // Проверка разницы между end_time и start_time
    const fortyDaysAgo = new Date(params["end_time"]);
    fortyDaysAgo.setDate(fortyDaysAgo.getDate() - 40);

    if (startDate < fortyDaysAgo) {
        params["start_time"] = fortyDaysAgo.toISOString().split('T')[0];
    } else {
        params["start_time"] = start_time;
    }

    return params;
}


async function progressBarTable(data) {
    const tableContainer = document.getElementById("progressBarTable");
    let progress = 0;

    while (progress < 99) {
        await  new Promise(resolve => setTimeout(resolve, 1000));
        try {
            let response = await fetch(`/get/progress/calc/${data.payload.task_id}`);
            let json = await response.json();
          // Обновляем отображение прогресса
            progress = json.progress.percent
            tableContainer.append(`//////`);
            
            
        } catch (error) {
            console.error('Ошибка:', error);
            break;
        }
    }
    tableContainer.innerHTML = `<div class="progress-bar" role="progressbar" style="width: ${progress}%;" aria-valuenow="${progress}" aria-valuemin="0" aria-valuemax="100" id="">${progress}%</div>`;
    await  new Promise(resolve => setTimeout(resolve, 1000));
    tableContainer.innerHTML = ""
}
document.getElementById('exportButton').addEventListener('click', async function() {
    console.log(exp_data);
    if (code === 0) {
        code = 1;
        
        let start_time = document.getElementById("start_time").value;
        let end_time = document.getElementById("end_time").value;
        let search_input = document.getElementById('search-input').value;
        let params = empReport(start_time, end_time);
        start_time = params["start_time"];
        end_time = params["end_time"];
        let url;

        if (search_input) {
            url = `/api/get_emp_report/?start_date=${start_time}&end_date=${end_time}&employees=${search_id}&exp_data=true`;
        } else {
            url = `/api/get_emp_report/?start_date=${start_time}&end_date=${end_time}&exp_data=true`;
        }

        try {
            // Отправляем запрос на сервер для получения файла
            let response = await fetch(url, {
                method: 'GET'
            });

            if(response.status === 403){
                alert("Срок сессии истёк")
                logout()
            }
            else if (!response.ok) {
                throw new Error(`Ошибка HTTP: ${response.status}`);
                
            }else{

            // Преобразуем ответ в Blob для загрузки файла
            const blob = await response.blob();
            const downloadUrl = URL.createObjectURL(blob);

            // Создаём элемент <a> для скачивания файла
            const a = document.createElement('a');
            a.href = downloadUrl;
            a.download = `${start_time}_${end_time}.xlsx`; // Устанавливаем имя файла
            document.body.appendChild(a);
            a.click();
            
            // Удаляем элемент и освобождаем URL после загрузки
            a.remove();
            URL.revokeObjectURL(downloadUrl);
        }} catch (error) {
            console.error('Ошибка при получении файла:', error);
        } finally {
            // Сброс значения code после завершения процесса
            code = 0;
        }
    }
});

// document.getElementById('submitCount').addEventListener('click', function() {


//     if (code === 0) {
//         code = 1; 
//         let start_time = document.getElementById("start_time").value;
//         let end_time = document.getElementById("end_time").value;
//         let table_clear = document.getElementById("myTable");
//         table_clear.innerHTML = "";
//         let params = empReport(start_time, end_time);
//         start_time = params["start_time"];
//         end_time = params["end_time"];
//         // progressBarTable()
//         fetch(`/calc/${start_time}/${end_time}/`)
//         .then(response => response.json())
//         .then(data => {
//             progressBarTable(data);
//             console.log(data);
//             code = 0;
//         })
//         .catch(error => console.error('Ошибка:', error), code = 0);


        
    
//     }else{
//         alert("ЖДИ!!!");
//     }
    

// });

function formatTimeCell(cellData, code){
    let parts = cellData.split(' ')
    let time = '';
    let firsColor ='';
    let secondColor = '';

    if (code === 1){
        time = parts[1];
        firsColor = parts[0]
        return {"time": time, "firsColor": firsColor}
    } else if (code ===2){
        time = parts[0];
        secondColor = parts[1];
        return {"time": time, "secondColor": secondColor}
    } else if (code === 3){
        time = parts[1];
        firsColor = parts[0]
        secondColor = parts[2];
        return {"time": time, "firsColor": firsColor, "secondColor": secondColor}
    }

}

document.getElementById('formSearch').addEventListener('submit', async function(event) {
    event.preventDefault();
    
    if (code === 0) {
        code = 1;
        
        let start_time = document.getElementById("start_time").value;
        let end_time = document.getElementById("end_time").value;
        let search_input = document.getElementById('search-input');
        if (search_input){
            search_input = search_input.value
        }
        let table_clear = document.getElementById("myTable");
        table_clear.innerHTML = "";
        let params = empReport(start_time, end_time);
        start_time = params["start_time"];
        end_time = params["end_time"];
        
        let url;
        if (search_input) {
            url = `/api/get_emp_report/?start_date=${start_time}&end_date=${end_time}&employees=${search_id}`;
        } else {
            url = `/api/get_emp_report/?start_date=${start_time}&end_date=${end_time}`;
        }

        try {
            // Исправление: добавляем await для fetch
            let response = await fetch(url);

            // Проверка на успешный статус ответа
            if(response.status === 403){
                alert("Срок сессии истёк")
                logout()
            }
            else if (!response.ok) {
                throw new Error(`Ошибка HTTP: ${response.status}`);
                
            }else{

            // Парсим данные как JSON
            const data = await response.json();
            exp_data = data
            let table = document.getElementById('myTable');
            table.innerHTML = '';
            if(data.status_code){
                table_clear.innerHTML = `<h1>Ошибка: ${data.status_code} ${data.description}</h1>`;
            }else{
                // Создание заголовков таблицы
                const thead = table.createTHead();
                const headerRow = thead.insertRow();
                const header = ["ИМЯ"];
                let current_date = new Date(start_time);
                const end_date = new Date(end_time);
                thead.classList.add("sticky-top");
    
                while (current_date <= end_date) {
                    let day = current_date.getDate();
                    if (day < 10){day = `0${day}`;}
                    let month = current_date.getMonth() + 1;
                    if (month < 10){month = `0${month}`}
                    header.push(`${day}.${month}`);
                    current_date.setDate(current_date.getDate() + 1);
                }
    
                const LIST_HEADERS = ["Обычный", "Опоздание", "Уход раньше", "Нарушения", "Неявка"];
                header.push(...LIST_HEADERS);
    
                header.forEach(headerText => {
                    const cell = headerRow.insertCell();
                    cell.textContent = headerText;
                    cell.style.fontWeight = "bold";
                    cell.style.backgroundColor = "#4F81BD";
                    cell.style.color = "#FFFFFF";
                    cell.style.textAlign = "center";
                    cell.style.border = "1px solid black";
                    cell.classList.add("sticky-top");
                });
    
                // Создаем tbody
                const tbody = table.createTBody();
    
                // Заполнение данных таблицы
                data.forEach(rowData => {
                    const row = tbody.insertRow();
    
                    rowData.forEach(cellData => {
                        const cell = row.insertCell();
                        cell.textContent = cellData;
    
                        if (cellData === 'Н') {
                            cell.classList.add('highlight-red');
                        } else if (cellData.includes(' - Н')) {
                            cell.classList.add('highlight-yellow');
                        } else if (cellData.includes('#E535FD') && cellData.includes('#34A7FE')) {
                            let response = formatTimeCell(cellData, code=3)
                            cell.textContent = response.time
                            cell.classList.add('highlight-gradient-blue');
                        }else if (cellData.includes('#E535FD')) {
                            let response = formatTimeCell(cellData, code=1)
                            cell.textContent = response.time;
                            cell.classList.add('highlight-purple');
                        }else if (cellData.includes('#34A7FE')) {
                            let response = formatTimeCell(cellData, code=2)
                            cell.textContent = response.time
                            cell.classList.add('highlight-blue');
                        }else if (cellData.includes("#002060")) {
                            let response = formatTimeCell(cellData, code=1)
                            cell.textContent = response.time;
                            cell.classList.add('highlight-siny');
                    };
                    })
                });

            }
            
            code = 0;

        }} catch (error) {
            console.error('Error:', error);
            code = 0;
            table_clear.innerHTML = `<h1>Ошибка: ${error.message} Обратитесь к администратору</h1>`;
        }
    } else {
        alert("ЖДИ!!!");
    }
});

