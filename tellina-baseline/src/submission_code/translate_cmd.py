from website import backend_interface


def translate_clai(request_str):
    global layers_top_k_scores
    trans_list = []
    annotated_trans_list = []

    if not trans_list:
        # call learning model and store the translations
        batch_outputs, output_logits = backend_interface.translate_fun(request_str)

        if batch_outputs:
            top_k_predictions = batch_outputs[0]
            top_k_scores = output_logits[0]
            layers_top_k_scores = []

            # Storing all layer scores into an array
            for i in range(len(output_logits)):
                layers_top_k_scores.append(output_logits[i])

    # tellina_top_response_cmd = top_k_predictions[0][1]

    ## Need to change the return

    # tellina_return = {
    #     'response': tellina_top_response_cmd,
    #     'confidence': '0.0'
    # }
    # return tellina_return

    return top_k_predictions, top_k_scores, layers_top_k_scores


def main():
    req_string = "show me all files in this directory"
    preds, scores, layers = translate_clai(req_string)
    print(preds)


if __name__ == '__main__':
    main()
