import { useState } from 'react';
import pikavee from './assets/pikavee.png';
import god from './assets/god.png';
import woogonite from './assets/woogonite.png';
import zaviper from './assets/zaviper.png';
import ironBird from './assets/iron_bird.png';
import rapidale from './assets/rapidale.png';
import pikarisu from './assets/pikarisu.png';
import silcoon from './assets/silcoon.png';

const SPRITE = 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon';

const EXAMPLES = [
  { fusion: pikavee,   name: 'Pikavee',   p1: { id: 25,  name: 'Pikachu'     }, p2: { id: 133, name: 'Eevee'      } },
  { fusion: god,       name: 'God',       p1: { id: 399, name: 'Bidoof'       }, p2: { id: 493, name: 'Arceus'     } },
  { fusion: woogonite, name: 'Woogonite', p1: { id: 831, name: 'Wooloo'       }, p2: { id: 149, name: 'Dragonite'  } },
  { fusion: zaviper,   name: 'Zaviper',   p1: { id: 335, name: 'Zangoose'     }, p2: { id: 336, name: 'Seviper'    } },
  { fusion: ironBird,  name: 'Iron Bird', p1: { id: 991, name: 'Iron Bundle'  }, p2: { id: 225, name: 'Delibird'   } },
  { fusion: rapidale,  name: 'Rapidale',  p1: { id: 77,  name: 'Rapidash'     }, p2: { id: 749, name: 'Mudsdale'   } },
  { fusion: pikarisu,  name: 'Pikarisu',  p1: { id: 25,  name: 'Pikachu'      }, p2: { id: 417, name: 'Pachirisu'  } },
  { fusion: silcoon,   name: 'Silcoon²',  p1: { id: 266, name: 'Silcoon'      }, p2: { id: 268, name: 'Cascoon'    } },
];

function PokemonTile({ src, name, pixelated = false }) {
  return (
    <div style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '8px' }}>
      <div style={{ width: '100%', aspectRatio: '1', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <img
          src={src}
          alt={name}
          style={{
            width: '100%',
            height: '100%',
            objectFit: 'contain',
            imageRendering: pixelated ? 'pixelated' : 'auto',
          }}
        />
      </div>
      <span style={{ fontSize: '1rem', color: '#555', textAlign: 'center' }}>{name}</span>
    </div>
  );
}

function Symbol({ char }) {
  return (
    <span style={{
      fontSize: '2rem',
      color: '#aaa',
      flexShrink: 0,
      alignSelf: 'center',
      padding: '0 8px',
      paddingBottom: '28px',
    }}>
      {char}
    </span>
  );
}

function EquationRow({ example }) {
  return (
    <div style={{
      display: 'flex',
      alignItems: 'flex-end',
      width: '100%',
      padding: '24px 16px',
      border: '1px solid #eee',
      borderRadius: '8px',
      background: '#fafafa',
      boxSizing: 'border-box',
    }}>
      <PokemonTile src={`${SPRITE}/${example.p1.id}.png`} name={example.p1.name} pixelated />
      <Symbol char="+" />
      <PokemonTile src={`${SPRITE}/${example.p2.id}.png`} name={example.p2.name} pixelated />
      <Symbol char="=" />
      <PokemonTile src={example.fusion} name={example.name} />
    </div>
  );
}

export default function ExamplesSection() {
  const [idx, setIdx] = useState(0);

  function prev() { setIdx(i => (i - 1 + EXAMPLES.length) % EXAMPLES.length); }
  function next() { setIdx(i => (i + 1) % EXAMPLES.length); }

  return (
    <section style={{ marginTop: '56px', width: '100%' }}>
      <h2 style={{ textAlign: 'center', marginBottom: '24px', fontSize: '1.4rem', fontWeight: 600 }}>
        Example Fusions
      </h2>

      <div style={{ display: 'flex', alignItems: 'center', width: '100%', gap: '12px' }}>
        <button onClick={prev} style={arrowStyle}>&#8592;</button>
        <div style={{ flex: 1 }}>
          <EquationRow example={EXAMPLES[idx]} />
        </div>
        <button onClick={next} style={arrowStyle}>&#8594;</button>
      </div>

      <div style={{ textAlign: 'center', marginTop: '12px', fontSize: '1rem', color: '#aaa' }}>
        {idx + 1} / {EXAMPLES.length}
      </div>
    </section>
  );
}

const arrowStyle = {
  background: 'none',
  border: '1px solid #ccc',
  borderRadius: '50%',
  width: '44px',
  height: '44px',
  fontSize: '20px',
  cursor: 'pointer',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  flexShrink: 0,
};
