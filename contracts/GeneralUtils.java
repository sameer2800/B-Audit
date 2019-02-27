package com.credits.baudit.contracts;

import java.time.Instant;
import java.util.ArrayList;
import java.util.Date;

public class GeneralUtils {
	
	//this function  sorts all bids based on the ratings of the contractors and their bid values.
	//Also, we can apply some machine learning algos here to evolve the utility.
	public static AuctionBid selectBestBid(ArrayList<AuctionBid> bids) {		
		return bids.get(0);
	}

	public static boolean isFaultyDevice(Device device) {
		if(device.getPurchaseDate().before(Date.from(Instant.now()))) {
			return true;
		}
		return false;
	}
	
}
