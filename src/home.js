import React, { useState, useEffect } from 'react'
import NavBar from './navbar'
import { useLocation } from 'react-router-dom';
import './home.css';
import MusicSection from './musicSection';
import QuerySection from './querySection';
import UserSection from './userSection';

export default function Home() {
 const location = useLocation();
 const email = location?.state?.email;
 let API_URL =  "https://3jzllb3tfg.execute-api.us-east-1.amazonaws.com/staging/";

  const [homeData, setHomeData] = useState(null);
  const [username, setUsername] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  
  // Fetch home data from API.
  useEffect(() => {
    async function fetchData() {

      // Making a POST request with the email to get the username and subscribed songs.
      try {   
        const response_username = await fetch(API_URL+"home", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: email
            })
        });

        if (!response_username.ok) {
            throw new Error('Network response was not ok');
        }

        const username_and_songs = await response_username.json();
        const data_username = username_and_songs['user_name'];
        const data_music = username_and_songs['subscribed_songs'];

        // Set the state with the username and subscribed songs.
        setUsername(data_username);
        setHomeData(data_music);
        setIsLoading(false);
        console.log(data_music)
        console.log(homeData)

      } catch (error) {
          console.error('Error fetching home data:', error);
          setIsLoading(false);
        }
    }

    fetchData();
  }, [email]);
  useEffect(() => {
    console.log('Home data updated:', homeData);
  }, [homeData]);

  // Function to handle the unsubscribe button by making a PATCH request to the API.
  const handleUnsubscribe = async (song_name) => {
    const requestOptions = {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, song_name, action: 'unsubscribe' }),
    };

    try {
      const response = await fetch(
        'https://3jzllb3tfg.execute-api.us-east-1.amazonaws.com/staging/home',
        requestOptions
      );

      // Handle successful unsubscribe. 
      if (response.ok) {
        const newHomeData = homeData.filter(
          (music) => `${music.title}-${music.artist}` !== song_name
        );
        setHomeData(newHomeData);

      } else {
        console.error('Error unsubscribing from the song');
      }

    } catch (error) {
      console.error('Error unsubscribing from the song:', error);
    }
  };
  
  // Function to handle the subscribe button by making a PATCH request to the API.
  const handleSubscribe = async (song_name, query_data) => {
    const requestOptions = {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, song_name, action: 'subscribe' }),
    };

    try {
      const response = await fetch(
        'https://3jzllb3tfg.execute-api.us-east-1.amazonaws.com/staging/home',
        requestOptions
      );

      // Handle successful subscribe. 
      // NOTE: queryData is returned from the querySection.js component. It contains the newly subscribed song from the query.
      if (response.ok) {
        const newMusic = query_data.find(
          (music) => `${music.title}-${music.artist}` === song_name
        );
        console.log("NEW MUSIC: ", newMusic);
        
        // Appending the new song to the homeData state and creating a new state called newHomeData. And setting the homeData state to the newHomeData state.
        if (newMusic) {
          console.log("ADDING QUERY RESULT TO HOME DATA");
          const newHomeData = [...homeData, newMusic];
          setHomeData(newHomeData);
        }

        console.log("HOME DATA: ", homeData);

      } else {
        console.error('Error subscribing from the song');
      }
    } catch (error) {
      console.error('Error subscribing from the song:', error);
    }
  };


  // Rendering the home page.
  return (
    <div className='main_content'>
        <NavBar />
        <UserSection username={username} />
        <MusicSection homeData={homeData} isLoading={isLoading} onUnsubscribe={handleUnsubscribe} />        
        <QuerySection email={email} onSubscribe={handleSubscribe} isLoading={isLoading} />
    </div>
  )
}