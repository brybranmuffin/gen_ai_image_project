import { useState, useEffect, useRef } from 'react';

export function formatPokemon(p) {
  const name = p.name.charAt(0).toUpperCase() + p.name.slice(1);
  return `#${String(p.id).padStart(4, '0')} ${name}`;
}

export default function PokemonSearch({ pokemonList, selected, onSelect }) {
  const [query, setQuery] = useState('');
  const [isOpen, setIsOpen] = useState(false);
  const containerRef = useRef(null);

  useEffect(() => {
    function handleMouseDown(e) {
      if (containerRef.current && !containerRef.current.contains(e.target)) {
        setIsOpen(false);
      }
    }
    document.addEventListener('mousedown', handleMouseDown);
    return () => document.removeEventListener('mousedown', handleMouseDown);
  }, []);

  const inputValue = selected ? formatPokemon(selected) : query;

  const filtered = pokemonList.filter(p => {
    const q = selected ? '' : query.toLowerCase();
    if (!q) return true;
    return p.name.toLowerCase().includes(q) || String(p.id).includes(q);
  });

  function handleChange(e) {
    setQuery(e.target.value);
    if (selected) onSelect(null);
    setIsOpen(true);
  }

  function handleFocus() {
    setIsOpen(true);
  }

  function handleSelect(p) {
    onSelect(p);
    setQuery('');
    setIsOpen(false);
  }

  return (
    <div ref={containerRef} style={{ position: 'relative', width: '100%' }}>
      <input
        type="text"
        value={inputValue}
        onChange={handleChange}
        onFocus={handleFocus}
        placeholder="Search Pokémon…"
        style={{ width: '100%', boxSizing: 'border-box', padding: '6px 8px', fontSize: '14px' }}
      />
      {isOpen && filtered.length > 0 && (
        <ul style={{
          position: 'absolute',
          top: '100%',
          left: 0,
          right: 0,
          maxHeight: '240px',
          overflowY: 'auto',
          margin: 0,
          padding: 0,
          listStyle: 'none',
          border: '1px solid #ccc',
          background: '#fff',
          zIndex: 100,
        }}>
          {filtered.map(p => (
            <li
              key={p.id}
              onMouseDown={() => handleSelect(p)}
              style={{ padding: '5px 8px', cursor: 'pointer', fontSize: '14px' }}
              onMouseEnter={e => e.currentTarget.style.background = '#f0f0f0'}
              onMouseLeave={e => e.currentTarget.style.background = ''}
            >
              {formatPokemon(p)}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
