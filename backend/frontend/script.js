const realInput =
    document.getElementById("realSignature");

const doubtInput =
    document.getElementById("doubtSignature");


realInput.addEventListener("change", function() {

    const file = this.files[0];

    if (file) {

        document.getElementById(
            "realPreview"
        ).src = URL.createObjectURL(file);

    }

});


doubtInput.addEventListener("change", function() {

    const file = this.files[0];

    if (file) {

        document.getElementById(
            "doubtPreview"
        ).src = URL.createObjectURL(file);

    }

});


async function analyzeSignature() {

    const real =
        realInput.files[0];

    const doubt =
        doubtInput.files[0];


    if (!real || !doubt) {

        alert(
            "Please upload both signatures."
        );

        return;

    }


    const formData = new FormData();

    formData.append(
        "real_signature",
        real
    );

    formData.append(
        "doubted_signature",
        doubt
    );


    document.getElementById(
        "result"
    ).innerHTML =
        "<h2>🔍 AI ANALYZING...</h2>";


    try {

        const response =
            await fetch(
                "http://127.0.0.1:8000/analyze",
                {
                    method: "POST",
                    body: formData
                }
            );


        const data =
            await response.json();


        const a =
            data.analysis;


        document.getElementById(
            "result"
        ).innerHTML = `

            <div class="result-card">

                <h2>AI ANALYSIS COMPLETE</h2>

                <h1>
                    ${a.similarity}%
                </h1>

                <p>
                    Signature Similarity
                </p>

                <hr>

                <p>
                    Forgery Risk:
                    <b>${a.forgery_risk}%</b>
                </p>

                <p>
                    Pixel Match:
                    ${a.pixel_similarity}%
                </p>

                <p>
                    Shape Match:
                    ${a.shape_similarity}%
                </p>

                <p>
                    Stroke Match:
                    ${a.stroke_similarity}%
                </p>

                <h2>
                    ${a.result}
                </h2>

            </div>
        `;

    }

    catch (error) {

        document.getElementById(
            "result"
        ).innerHTML =
            "<p>Unable to connect to AI backend.</p>";

        console.error(error);

    }

}