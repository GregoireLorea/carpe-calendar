const addDate = document.getElementById('add-date');
const datesContainer = document.getElementById('dates-container');

addDate.addEventListener('click', function() {
    const dateForm = document.createElement('div');
    dateForm.classList.add('form-group');
    dateForm.innerHTML = `
        <div class="mb-3 form-row align-items-center date-form-container">
            <div class="col-sm-3 my-1">
                <label for="start" class="form-label">Début</label>
                <input type="datetime-local" name="start" id="start" class="form-control">
            </div>
            <div class="col-sm-3 my-1">
                <label for="end" class="form-label">Fin</label>
                <input type="datetime-local" name="end" id="end" class="form-control">
            </div>
        </div>
    `;
    datesContainer.appendChild(dateForm);
});
