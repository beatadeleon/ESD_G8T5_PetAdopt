<template>
  <div>
    <h1>Book Meeting</h1>
    <div id="calendly-embed" style="min-width:320px;height:700px;"></div>
  </div>
</template>

<script>
export default {
  mounted() {
    // Include the Calendly JavaScript file
    const script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = 'https://assets.calendly.com/assets/external/widget.js';
    document.head.appendChild(script);

    // Use the API call to initialize the inline widget
    Calendly.initInlineWidget({
      url: 'https://calendly.com/chooyining-sg/adoption-suitability-assesment',
      parentElement: document.getElementById('calendly-embed'),
      prefill: {},
      utm: {}
    });

    function isCalendlyEvent(e) {
      return e.origin === "https://calendly.com" && e.data.event && e.data.event.indexOf("calendly.") === 0;
    }

    window.addEventListener("message", async function (e) {
      if (isCalendlyEvent(e) && e.data.event === "calendly.event_scheduled") {
        try {
          // Extract the email from the event payload
          const userEmail = e.data.payload.invitee.email;
          const calendlyUuid = e.data.payload.uuid;

          // Fetch the user ID from your backend
          fetch('http://localhost:5100/get_user_id', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email: userEmail })
          })
          .then(response => response.json())
          .then(data => {
            if (data.userId) {
              // With the userId, send another request to update the booking
              const updateRequestBody = {
                userId: data.userId,
                calendlyUuid: calendlyUuid
              };

              return fetch('http://localhost:5100/update_booking', {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json'
                },
                body: JSON.stringify(updateRequestBody)
              });
            } else {
              throw new Error('User ID not found for the given email');
            }
          })
          .then(updateResponse => updateResponse.json())
          .then(updateData => {
            console.log("Booking updated with UUID: ", updateData);
          })
          .catch((error) => {
            console.error("Error updating the booking: ", error);
          });

        } catch (error) {
          console.error("Error handling Calendly event:", error);
        }
      }
    });
  }
};
</script>