function delete_post(id) {
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = '/delete';
  
    const input = document.createElement('input');
    input.type = 'hidden';
    input.name = 'id';
    input.value = id;
  
    form.appendChild(input);
    document.body.appendChild(form);
    form.submit();
}

function like(id) {
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = '/like';
  
    const input = document.createElement('input');
    input.type = 'hidden';
    input.name = 'id';
    input.value = id;
  
    form.appendChild(input);
    document.body.appendChild(form);
    form.submit();
}

function dislike(id) {
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = '/dislike';
  
    const input = document.createElement('input');
    input.type = 'hidden';
    input.name = 'id';
    input.value = id;
  
    form.appendChild(input);
    document.body.appendChild(form);
    form.submit();
}

function goProf(id) {
    const form = document.createElement('form');
    form.method = 'GET';
    form.action = '/profile';
  
    const input = document.createElement('input');
    input.type = 'hidden';
    input.name = 'id';
    input.value = id;
  
    form.appendChild(input);
    document.body.appendChild(form);
    form.submit();
}