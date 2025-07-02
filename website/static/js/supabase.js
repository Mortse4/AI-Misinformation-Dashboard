
import { createClient } from '@supabase/supabase-js'

document.addEventListener("DOMContentLoaded", function() {
    // Create a single Supabase client for interacting with your database
    const supabase = createClient("https://gjaeukqadjcskldqrsoy.supabase.co", 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdqYWV1a3FhZGpjc2tsZHFyc295Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTQ3NjA2NzAsImV4cCI6MjAzMDMzNjY3MH0.0NQ6oEMsKBqsT0cNyxsvQ3SUU5-QhIR_OORDCuZM6bQ');

    // Function to fetch topics from Supabase
    async function fetchTopics() {
        const { data, error } = await supabase
            .from('topics')
            .select('*'); // Select all columns from 'topics' table

        if (error) {
            console.error('Error fetching data:', error.message);
            return;
        }

        // Process the retrieved data and update the HTML template
        renderTopics(data);
    }

    // Function to update HTML template with topics data
    function renderTopics(topics) {
        const container = document.querySelector('.box-container');
        container.innerHTML = ''; // Clear previous content

        topics.forEach(topic => {
            const topicHTML = `
                <div class="box">
                    <div class="image">
                        <a href="${topic.url}">
                            <img src="${topic.image}" alt="${topic.name}">
                        </a>
                    </div>
                    <div class="content">
                        <h3>${topic.name}</h3>
                        <div class="interactions">Total Engagement: ${topic.interactions}</div>
                        <div class="likes">Likes: ${topic.likesTotal}</div>
                        <div class="shares">Shares: ${topic.sharesTotal}</div>
                        <div class="comments">Comments: ${topic.commentsTotal}</div>
                        <div class="date">Date: ${topic.date}</div>
                    </div>
                </div>
            `;
            container.insertAdjacentHTML('beforeend', topicHTML);
        });
    }

    // Fetch topics when the page loads
    fetchTopics();
});
