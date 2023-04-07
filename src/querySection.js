import React, { useState } from 'react';
import './querySection.css';

function QuerySection({ email, onSubscribe, isLoading }) {
    const [title, setTitle] = useState('');
    const [year, setYear] = useState('');
    const [artist, setArtist] = useState('');
    const [queryData, setQueryData] = useState([]);

    // Calling the handleSubscribe from home.js.
    const handleSubscribe = (song_name, queryData) => {

        // Create a copy of queryData
        const tempQueryData = [...queryData]

        // Remove subscribed somg from form queryData so that it is rendered again in the query section.
        const index = queryData.findIndex((song) => `${song.title}-${song.artist}` === song_name);
        queryData.splice(index, 1);

        // Passing the song name and data of the newly subscribed song to handleSubscribe from home.js.
        onSubscribe(song_name, tempQueryData);
    };

    // Calling the API to query the database based on search parameters entered by the user.
    const handleQuery = async () => {

        // Check if title, artist, year are empty. If so, return an error.
        if (title === '' && artist === '' && year === '') {
            alert('Please enter at least one search parameter');
            return;
        }

        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, title, artist, year }),
        };

        try {
            const response = await fetch('https://3jzllb3tfg.execute-api.us-east-1.amazonaws.com/staging/home', requestOptions);
            const data = await response.json();
            console.log("HERE IS THE QUERY RESULTS: ", data);

            // Check if the query returned any results. If not, print a message to the user.
            if (data.length === 0) {
                alert('No results found. Please try again.');
                return;
            }
            
            setQueryData(data);
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    };

    return (
        <div className="query-section">
            <h1> Query Section</h1>
            <label htmlFor="title">Title:</label>
            <input
                type="text"
                id="title"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
            />
            <label htmlFor="year">Year:</label>
            <input
                type="text"
                id="year"
                value={year}
                onChange={(e) => setYear(e.target.value)}
            />
            <label htmlFor="artist">Artist:</label>
            <input
                type="text"
                id="artist"
                value={artist}
                onChange={(e) => setArtist(e.target.value)}
            />
            <button onClick={handleQuery}>Query</button>

            {isLoading ? (
                <p>Loading...</p>
            ) : (
            <div className="musicList">
                {queryData.map((music) => (
                    <div key={music.title} className="musicItem">
                        <p>{music.title}</p>
                        <p>{music.artist}</p>
                        <p>{music.year}</p>
                        <img src={music.img_url} alt={music.artist} />
                        <button
                            onClick={() =>
                                handleSubscribe(`${music.title}-${music.artist}`, queryData)
                            }
                        >
                            Subscribe
                        </button>
                    </div>
                ))}
            </div>
            )}
        </div>
    );
}

export default QuerySection;