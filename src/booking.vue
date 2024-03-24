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

    script.onload = () => {
      // Use the API call to initialize the inline widget
      Calendly.initInlineWidget({
        url: 'https://calendly.com/chooyining-sg/adoption-suitability-assesment',
        parentElement: document.getElementById('calendly-embed'),
        prefill: {},
        utm: {}
      });
    };

    function isCalendlyEvent(e) {
      return e.origin === "https://calendly.com" && e.data.event && e.data.event.indexOf("calendly.") === 0;
    }

    window.addEventListener("message", async function (e) {
      if (isCalendlyEvent(e) && e.data.event === "calendly.event_scheduled") {
        try {
          const userEmail = e.data.payload.invitee.email;
          const calendlyUuid = e.data.payload.uuid;

          fetch('http://localhost:5100/update_calendly_uuid', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
              email: userEmail,
              calendlyUuid: calendlyUuid
            })
          })
          .then(response => {
            if (!response.ok) {
              throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
          })
          .then(updateData => {
            console.log("Calendly UUID updated: ", updateData);
          })
          .catch((error) => {
            console.error("Error updating the Calendly UUID: ", error);
          });
        } catch (error) {
          console.error("Error extracting the email and calendlyUuid: ", error);
        }
      }
    });
  }
};
</script>