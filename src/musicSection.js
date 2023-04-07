import React from 'react';
import './home.css';

function MusicSection({ homeData, isLoading, onUnsubscribe  }) {

    // Calling the handleUnsubscribe from home.js. 
    const handleUnsubscribe = (song_name) => {
      onUnsubscribe(song_name);
    };

    return (
        <div className='musicSection'>
            <h1>Subscriptions Section</h1>
            {isLoading ? (
                <p>Loading...</p>
            ) : (
            <div className='musicList'>
                {homeData.map((music) => (
                    <div key={music.title} className='musicItem'>
                        <p>{music.title}</p>
                        <p>{music.artist}</p>
                        <p>{music.year}</p>
                        <img src={music.img_url} alt={music.artist} />
                        <button
                          onClick={() =>
                            handleUnsubscribe(`${music.title}-${music.artist}`)
                          }
                        >
                          Unsubscribe
                        </button>
                    </div>
                ))}
            </div>
            )}
            <hr></hr>
        </div> 
    );
  }

export default MusicSection;