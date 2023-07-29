

function change_theme(theme) { 
  document.querySelector('html').setAttribute('data-theme', theme);
}

let links = null;

function update_link_list() {
  if (links == null) {
    links = document.querySelectorAll('a');
  }

  // search for correct thingy 
  let search_term = document.getElementById('search__text').value;
  let suggestions = document.getElementById('search__suggestions');

  if (search_term == '') {
    suggestions.innerHTML = '';
    return;
  }

  let found_terms_set = new Set();
  const search_terms = search_term.split(' ');
  for (let i = 0; i < links.length; i++){
    for (let j = 0; j < search_terms.length; j++) {
      if (links[i].text.toLowerCase().includes(search_terms[j].toLowerCase())) {
        found_terms_set.add(links[i]);
      }
    }
  }

  let found_terms = found_terms_set.values();
  suggestions.innerHTML = '';
  if (found_terms_set.size == 0) {
    suggestions.innerHTML = `"No results for <strong>${search_term}</strong>"`;
    return;
  }

  for (const term of found_terms) {
    let h = document.createElement('a');
    h.href = term.href;
    h.text = term.text;
    let d = document.createElement('div');
    d.appendChild(h)
    if (suggestions.childElementCount > 10) break;
    suggestions.appendChild(d);
  }

}
