import React, { useState } from 'react';

const App: React.FC = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<any[]>([]);

  const handleSearch = async () => {
    try {
      const response = await fetch(`https://your-opensearch-endpoint.com/search?q=${query}`);
      const data = await response.json();
      setResults(data.hits.hits);
    } catch (error) {
      console.error('Error fetching search results:', error);
    }
  };

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setQuery(event.target.value);
  };

  return (
    <div>
      <input type="text" value={query} onChange={handleInputChange} />
      <button onClick={handleSearch}>Search</button>
      <div>
        {results.map((result) => (
          <div key={result._id}>
            {/* Render your result data here */}
            {result._source.title}
          </div>
        ))}
      </div>
    </div>
  );
};

export default App;