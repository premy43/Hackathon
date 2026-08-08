const sampleEmail = `
Dear Student,

Your project presentation has been scheduled for 12 August at 10:00 AM.

Please submit your final project report before 10 August.
Attendance is mandatory.

Thank you.
`;


function loadSample() {

    document.getElementById("emailInput").value = sampleEmail;

}


function clearEmail() {

    document.getElementById("emailInput").value = "";

    document.getElementById("summary").innerText =
        "Your email summary will appear here.";

    document.getElementById("priority").innerText = "-";

    document.getElementById("category").innerText = "-";

    document.getElementById("spamRisk").innerText = "-";

    document.getElementById("sentiment").innerText = "-";

    document.getElementById("priorityReason").innerText = "";

    document.getElementById("reply").value = "";

    document.getElementById("tasks").innerHTML =
        "<li>No tasks yet</li>";

    document.getElementById("deadlines").innerHTML =
        "<li>No deadlines yet</li>";
}


async function analyzeEmail() {

    const email =
        document.getElementById("emailInput").value.trim();


    if (!email) {

        alert("Please enter an email first.");

        return;
    }


    const loading =
        document.getElementById("loading");

    loading.style.display = "block";


    try {

        const response = await fetch("/analyze", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                email: email
            })

        });


        const data = await response.json();


        if (data.error) {

            alert(data.error);

            return;
        }


        // SUMMARY

        document.getElementById("summary").innerText =
            data.summary;


        // PRIORITY

        document.getElementById("priority").innerText =
            data.priority;


        document.getElementById("priorityReason").innerText =
            data.priority_reason;


        // CATEGORY

        document.getElementById("category").innerText =
            data.category;


        // SPAM

        document.getElementById("spamRisk").innerText =
            data.spam_risk;


        // SENTIMENT

        document.getElementById("sentiment").innerText =
            data.sentiment;


        // TASKS

        const taskList =
            document.getElementById("tasks");

        taskList.innerHTML = "";

        data.tasks.forEach(task => {

            const li = document.createElement("li");

            li.innerText = task;

            taskList.appendChild(li);

        });


        // DEADLINES

        const deadlineList =
            document.getElementById("deadlines");

        deadlineList.innerHTML = "";

        data.deadlines.forEach(deadline => {

            const li = document.createElement("li");

            li.innerText = deadline;

            deadlineList.appendChild(li);

        });


        // REPLY

        document.getElementById("reply").value =
            data.reply;


    }

    catch (error) {

        alert(
            "Something went wrong. Please try again."
        );

        console.error(error);

    }

    finally {

        loading.style.display = "none";

    }

}


function copyReply() {

    const reply =
        document.getElementById("reply").value;


    if (!reply) {

        alert("No reply available.");

        return;
    }


    navigator.clipboard.writeText(reply)

        .then(() => {

            alert("Reply copied!");

        });

}
