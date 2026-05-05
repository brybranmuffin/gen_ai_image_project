import { useState, useEffect } from 'react';

export function usePokemonList() {
  const [list, setList] = useState([]);

  useEffect(() => {
    fetch('https://pokeapi.co/api/v2/pokemon?limit=1300')
      .then(r => r.json())
      .then(data => {
        const filtered = data.results
          .map(p => ({
            id: parseInt(p.url.split('/').filter(Boolean).pop(), 10),
            name: p.name,
          }))
          .filter(p => p.id >= 1 && p.id <= 1026 && p.id !== 696)
          .sort((a, b) => a.id - b.id);
        setList(filtered);
      });
  }, []);

  return list;
}
