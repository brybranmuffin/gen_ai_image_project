import { useState, useRef } from 'react';
import { usePokemonList } from './usePokemonList';
import PokemonPanel from './PokemonPanel';
import SliderPanel from './SliderPanel';
import ExamplesSection from './ExamplesSection';

const APIM_URL = 'https://pokae-api.azure-api.net/interpolate';
const APIM_KEY = import.meta.env.VITE_APIM_KEY ?? '';

export default function App() {
  const [leftPokemon, setLeftPokemon] = useState({ id: 25, name: "pikachu" });
  const [rightPokemon, setRightPokemon] = useState({ id: 133, name: "eevee" });
  const [sliderValue, setSliderValue] = useState(50);
  const [resultUrl, setResultUrl] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const pokemonList = usePokemonList();
  const prevUrlRef = useRef(null);

  async function handleGenerate() {
    if (!leftPokemon || !rightPokemon) return;
    setIsLoading(true);
    try {
      const alpha = sliderValue / 100;
      const url = `${APIM_URL}?pokedex_id_1=${leftPokemon.id}&pokedex_id_2=${rightPokemon.id}&alpha=${alpha}`;
      const resp = await fetch(url, {
        method: 'POST',
        headers: { 'Ocp-Apim-Subscription-Key': APIM_KEY },
      });
      if (!resp.ok) throw new Error(`API error ${resp.status}`);
      const blob = await resp.blob();
      const newUrl = URL.createObjectURL(blob);
      if (prevUrlRef.current) URL.revokeObjectURL(prevUrlRef.current);
      prevUrlRef.current = newUrl;
      setResultUrl(newUrl);
    } catch (err) {
      console.error('Generation failed:', err);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div style={{ width: '100%' }}>

      {/* Title — 50% wide, centered */}
      <div style={{ width: '50%', margin: '0 auto', textAlign: 'center', padding: '32px 0 24px' }}>
        <h1 style={{ margin: 0 }}>PokAE Machine</h1>
      </div>

      {/* Three equal columns, full width */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(3, 1fr)',
        width: '100%',
        alignItems: 'start',
      }}>
        <PokemonPanel
          pokemon={leftPokemon}
          onSelect={setLeftPokemon}
          pokemonList={pokemonList}
        />
        <SliderPanel
          sliderValue={sliderValue}
          setSliderValue={setSliderValue}
          leftPokemon={leftPokemon}
          rightPokemon={rightPokemon}
          onGenerate={handleGenerate}
          isLoading={isLoading}
          resultUrl={resultUrl}
        />
        <PokemonPanel
          pokemon={rightPokemon}
          onSelect={setRightPokemon}
          pokemonList={pokemonList}
        />
      </div>

      {/* Gallery — 50% wide, centered */}
      <div style={{ width: '50%', margin: '0 auto' }}>
        <ExamplesSection />
      </div>

      <footer style={{ marginTop: '48px', textAlign: 'center', fontSize: '13px', color: '#999', paddingBottom: '32px' }}>
        Pokémon data and sprites provided by{' '}
        <a href="https://pokeapi.co" target="_blank" rel="noreferrer" style={{ color: '#999' }}>
          PokéAPI
        </a>
        {' '}— used under the{' '}
        <a href="https://github.com/PokeAPI/pokeapi/blob/master/LICENSE.md" target="_blank" rel="noreferrer" style={{ color: '#999' }}>
          BSD licence
        </a>.
      </footer>
    </div>
  );
}
